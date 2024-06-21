import collections
import csv
import io
import json
import os
from collections import OrderedDict

import sphinxcontrib.jsonschema
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst.directives.tables import CSVTable
from jsonpointer import resolve_pointer
from sphinx.directives.code import LiteralInclude

from . import MARKDOWN_SUPPORT, CSVTableNoTranslate

if MARKDOWN_SUPPORT:
    from .markdown import parse_markdown


def flatten_dict(obj, path, result, recursive=False):
    if hasattr(obj, 'items'):
        for key, value in obj.items():
            if isinstance(value, dict):
                if recursive:
                    flatten_dict(value, path + '/' + key, result, recursive=recursive)
            elif isinstance(value, list):
                if isinstance(value[0], dict):
                    if recursive:
                        for num, sub_value in enumerate(value):
                            flatten_dict(sub_value, path + '/' + key + '/' + str(num), result, recursive=recursive)
                else:
                    result[path + '/' + key] = ", ".join(value)
            else:
                result[path + '/' + key] = value


class JSONInclude(LiteralInclude):
    option_spec = {
        'jsonpointer': directives.unchanged,
        'expand': directives.unchanged,
        'exclude': directives.unchanged,
        'include_only': directives.unchanged,
        'title': directives.unchanged,
    }

    def get_filename_and_pointed(self):
        env = self.state.document.settings.env
        dirname = os.path.dirname(env.doc2path(env.docname, base=None))
        relpath = os.path.join(dirname, self.arguments[0])
        abspath = os.path.join(env.srcdir, relpath)
        if not os.access(abspath, os.R_OK):
            raise self.warning('JSON file not readable: %s' %
                               self.arguments[0])

        with open(abspath) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        filename = str(self.arguments[0]).split("/")[-1].replace(".json", "")
        pointed = resolve_pointer(json_obj, self.options['jsonpointer'])
        return filename, pointed

    def run(self):
        filename, pointed = self.get_filename_and_pointed()

        try:
            title = self.options['title']
        except KeyError:
            title = filename

        # Remove the items mentioned in exclude
        if self.options.get('exclude'):
            for item in self.options['exclude'].split(","):
                try:
                    del pointed[item.strip()]
                except KeyError:
                    pass

        if self.options.get('include_only'):
            for node in list(pointed):
                if not (node in self.options.get('include_only')):
                    del pointed[node]

        code = json.dumps(pointed, indent='    ')
        # Ideally we would add the below to a data-expand element, but I can't see how to do this,
        # so using classes for now...
        class_list = self.options.get('class', [])
        class_list.append('file-' + title)
        expand = str(self.options.get("expand", "")).split(",")
        class_list = class_list + ['expandjson expand-{0}'.format(s.strip()) for s in expand]
        literal = nodes.literal_block(code, code)
        literal['language'] = 'json'
        container = nodes.container(classes=class_list)
        container += literal
        return [container]


class JSONIncludeQuote(JSONInclude):
    def run(self):
        filename, pointed = self.get_filename_and_pointed()
        block_quote = nodes.block_quote('')
        block_quote += parse_markdown(pointed, document=self.state.document)
        return [block_quote]


class JSONIncludeFlat(CSVTableNoTranslate):
    option_spec = CSVTable.option_spec.copy()
    option_spec['jsonpointer'] = directives.unchanged
    option_spec['title'] = directives.unchanged
    option_spec['exclude'] = directives.unchanged
    option_spec['include_only'] = directives.unchanged
    option_spec['recursive'] = directives.flag
    option_spec['ignore_path'] = directives.unchanged

    def make_title(self):
        return None, []

    def get_csv_data(self):
        env = self.state.document.settings.env
        dirname = os.path.dirname(env.doc2path(env.docname, base=None))
        relpath = os.path.join(dirname, self.arguments[0])
        abspath = os.path.join(env.srcdir, relpath)
        if not os.access(abspath, os.R_OK):
            raise self.warning('JSON file not readable: %s' %
                               self.arguments[0])

        with open(abspath) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        pointed = resolve_pointer(json_obj, self.options['jsonpointer'])
        if self.options.get('exclude'):
            for item in self.options['exclude'].split(","):
                try:
                    del pointed[item.strip()]
                except KeyError:
                    pass
        if self.options.get('include_only'):
            for node in list(pointed):
                if not (node in self.options.get('include_only')):
                    del pointed[node]
        csv_data = []

        ignore_path = self.options.get('ignore_path', ' ')

        if isinstance(pointed, dict):
            result = collections.OrderedDict()
            flatten_dict(pointed, self.options['jsonpointer'], result, 'recursive' in self.options)
            if ignore_path:
                csv_data.append([heading.replace(ignore_path, "") for heading in result.keys()])
            else:
                csv_data.append(result.keys())
            csv_data.append(list(result.values()))

        if isinstance(pointed, list):
            for row in pointed:
                result = collections.OrderedDict()
                flatten_dict(row, self.options['jsonpointer'], result, 'recursive' in self.options)
                csv_data.append(list(result.values()))
            if ignore_path:
                csv_data.insert(0, [heading.replace(ignore_path, "") for heading in result.keys()])
            else:
                csv_data.insert(0, result.keys())

        output = io.StringIO()
        output_csv = csv.writer(output)
        for line in csv_data:
            output_csv.writerow(line)
        self.options['header-rows'] = 1
        return output.getvalue().splitlines(), abspath


def type_format_simple(prop):
    prop_type = prop.attributes.get('type')
    if prop.format:
        return prop.format
    elif isinstance(prop_type, list) and len(prop_type) == 2 and prop_type[1] == 'null':
        return prop_type[0]
    else:
        return prop.type


class JSONSchemaTitlesDirective(sphinxcontrib.jsonschema.JSONSchemaDirective):
    headers = ['Title', 'Description', 'Type', 'Required']
    widths = [1, 3, 1, 1]
    option_spec = {
        'child': directives.unchanged,
    }
    child = None

    def make_nodes(self, schema):
        child = self.options.get('child')
        if child:
            for prop in schema:
                if prop.name == child:
                    return [nodes.paragraph('', nodes.Text(prop.description)), self.table(prop)]
            else:
                raise KeyError
        else:
            return [self.table(schema)]

    def row(self, prop, tbody):
        # Don't display rows for objects and arrays of objects (only their children)
        if (
            isinstance(prop, sphinxcontrib.jsonschema.Object)
            or (isinstance(prop, sphinxcontrib.jsonschema.Array) and prop.items.get('type') == 'object')
        ):
            return
        if not prop.rollup and prop.parent.parent.name != self.options.get('child'):
            return
        row = nodes.row()
        row += self.cell(prop.full_title)
        row += self.cell(prop.description or '')
        row += self.cell(type_format_simple(prop))
        row += self.cell(prop.required)
        tbody += row


class JSONSchemaTitleFieldnameMapDirective(sphinxcontrib.jsonschema.JSONSchemaDirective):
    headers = ['Title', 'Name', 'Type']
    widths = [1, 1, 1]

    def row(self, prop, tbody):
        # Don't display rows for objects and arrays of objects (only their children)
        if (isinstance(prop, sphinxcontrib.jsonschema.Object) or
            (isinstance(prop, sphinxcontrib.jsonschema.Array) and
                prop.items.get('type') == 'object')):
            return
        row = nodes.row()
        row += self.cell(prop.full_title)
        row += self.cell(prop.name)
        row += self.cell(type_format_simple(prop))
        tbody += row


class JSONSchemaArrayDirective(sphinxcontrib.jsonschema.JSONSchemaDirective):
    headers = ['', 'Description', 'Type', 'Required']
    widths = [1, 10, 2, 2]

    def row(self, prop, tbody):
        # Don't display rows for arrays and objects (only their children)
        if isinstance(prop, (sphinxcontrib.jsonschema.Array, sphinxcontrib.jsonschema.Object)):
            return

        assert prop.name.startswith('/0/')
        name = prop.name[3:]
        name_cell = nodes.entry('', nodes.literal('', nodes.Text(name)), morecols=3)

        row = nodes.row()
        row += name_cell
        tbody += row

        row = nodes.row()
        row += self.cell('')
        row += self.cell(prop.description or '')
        row += self.cell(type_format_simple(prop))
        row += self.cell(prop.required)
        tbody += row
