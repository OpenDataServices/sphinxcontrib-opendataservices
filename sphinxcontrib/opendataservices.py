import io
import os
import csv
import json
import collections
from collections import OrderedDict

from jsonpointer import resolve_pointer

import sphinxcontrib.jsonschema

from recommonmark.transform import AutoStructify
from recommonmark.parser import CommonMarkParser
from sphinx.directives.code import LiteralInclude
from docutils import nodes
from docutils.utils import new_document
from docutils.parsers.rst import directives, Directive
from docutils.parsers.rst.directives.tables import CSVTable


class AutoStructifyLowPriority(AutoStructify):
    """
    We need this low priority copy of AutoStructify to apply some transforms
    after translations.
    """
    default_priority = 1000


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

    def run(self):
        with open(self.arguments[0]) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        filename = str(self.arguments[0]).split("/")[-1].replace(".json", "")
        try:
            title = self.options['title']
        except KeyError as e:
            title = filename
        pointed = resolve_pointer(json_obj, self.options['jsonpointer'])
        # Remove the items mentioned in exclude
        if(self.options.get('exclude')):
            for item in self.options['exclude'].split(","):
                try:
                    del pointed[item.strip()]
                except KeyError as e:
                    pass

        if(self.options.get('include_only')):
            for node in list(pointed):
                if not (node in self.options.get('include_only')):
                    del pointed[node]

        code = json.dumps(pointed, indent='    ')
        # Ideally we would add the below to a data-expand element, but I can't see how to do this, so using classes for now...
        class_list = self.options.get('class', [])
        class_list.append('file-' + title)
        expand = str(self.options.get("expand", "")).split(",")
        class_list = class_list + ['expandjson expand-{0}'.format(s.strip()) for s in expand]
        literal = nodes.literal_block(code, code)
        literal['language'] = 'json'
        container = nodes.container(classes=class_list)
        container += literal
        return [container]


class JSONIncludeFlat(CSVTable):
    option_spec = {
        'jsonpointer': directives.unchanged,
        'title': directives.unchanged,
        'exclude': directives.unchanged,
        'include_only': directives.unchanged,
        'recursive': directives.flag,
        'ignore_path': directives.unchanged,
    }

    def make_title(self):
        return None, []

    def get_csv_data(self):
        file_path = self.arguments[0]
        with open(file_path) as fp:
            json_obj = json.load(fp, object_pairs_hook=OrderedDict)
        pointed = resolve_pointer(json_obj, self.options['jsonpointer'])
        if(self.options.get('exclude')):
            for item in self.options['exclude'].split(","):
                try:
                    del pointed[item.strip()]
                except KeyError as e:
                    pass
        if(self.options.get('include_only')):
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
        return output.getvalue().splitlines(), file_path


class CSVTableNoTranslate(CSVTable):
    def get_csv_data(self):
        lines, source = super().get_csv_data()
        return lines, None


class DirectoryListDirective(Directive):
    option_spec = {
        'path': directives.unchanged,
        'url': directives.unchanged,
    }

    def run(self):
        bl = nodes.bullet_list()
        for fname in os.listdir(self.options.get('path')):
            bl += nodes.list_item('', nodes.paragraph('', '', nodes.reference('', '',
                nodes.Text(fname),
                internal=False,
                refuri=self.options.get('url') + fname, anchorname='')))
        return [bl]


def parse_markdown(text):
        parser = CommonMarkParser()
        new_doc = new_document(None)  # , self.document.settings)
        parser.parse(text, new_doc)
        return new_doc.children[:]


class MarkdownDirective(Directive):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return parse_markdown(text)


class LiteralAndParsedMarkdownDirective(Directive):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return [
            nodes.paragraph('', '', nodes.Text('Source:')),
            nodes.literal_block(text, text),
            nodes.paragraph('', '', nodes.Text('Output:')),
        ] + parse_markdown(text)


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
        # Don't display rows for arrays and objects (only their children)
        if isinstance(prop, (sphinxcontrib.jsonschema.Array, sphinxcontrib.jsonschema.Object)):
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
        # Don't display rows for arrays and objects (only their children)
        if isinstance(prop, (sphinxcontrib.jsonschema.Array, sphinxcontrib.jsonschema.Object)):
            return
        row = nodes.row()
        row += self.cell(prop.full_title)
        row += self.cell(prop.name)
        row += self.cell(type_format_simple(prop))
        tbody += row


def setup(app):
    app.add_directive('csv-table-no-translate', CSVTableNoTranslate)
    app.add_directive('directory_list', DirectoryListDirective)
    app.add_directive('jsoninclude', JSONInclude)
    app.add_directive('jsoninclude-flat', JSONIncludeFlat)
    app.add_directive('markdown', MarkdownDirective)
    app.add_directive('literal-and-parsed-markdown', LiteralAndParsedMarkdownDirective)
    app.add_directive('jsonschema-titles', JSONSchemaTitlesDirective)
    app.add_directive('jsonschema-title-fieldname-map', JSONSchemaTitleFieldnameMapDirective)
