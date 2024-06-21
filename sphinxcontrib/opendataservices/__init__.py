import os

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.parsers.rst.directives.admonitions import Note
from docutils.parsers.rst.directives.tables import CSVTable
from docutils.parsers.rst.roles import set_classes
from docutils.transforms import Transform
from docutils.utils import SystemMessagePropagation
from sphinx import addnodes

try:
    import jsonpointer  # noqa
    JSON_SUPPORT = True
except ModuleNotFoundError:
    JSON_SUPPORT = False
try:
    import myst_parser  # noqa
    MARKDOWN_SUPPORT = True
except ModuleNotFoundError:
    MARKDOWN_SUPPORT = False


if MARKDOWN_SUPPORT:
    from .markdown import parse_markdown


# Based on positive_int_list from docutils
def nonnegative_int_list(argument):
    """
    Converts a space- or comma-separated list of values into a Python list
    of integers.
    (Directive option conversion function.)

    Raises ValueError for non-positive-integer values.
    """
    if ',' in argument:
        entries = argument.split(',')
    else:
        entries = argument.split()
    return [directives.nonnegative_int(entry) for entry in entries]


class CSVTableNoTranslate(CSVTable):
    option_spec = CSVTable.option_spec.copy()
    option_spec['included_cols'] = nonnegative_int_list

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        rows, max_cols = super().parse_csv_data_into_rows(csv_data, dialect, source)
        if 'included_cols' not in self.options:
            return rows, max_cols

        new_rows = []
        for row in rows:
            try:
                new_rows.append([row[i] for i in self.options['included_cols']])
            except IndexError:
                error = self.state_machine.reporter.error(
                    'One or more indexes of included_cols are not valid. '
                    'The CSV data does not contain that many columns.')
                raise SystemMessagePropagation(error)

        return new_rows, len(self.options['included_cols'])

    def run(self):
        returned = super().run()

        # docutils.parsers.rst.directives.tables.CSVTable.run() returns the nodes.table() node as the first node.
        table_node = returned[0]

        def is_text_element(node):
            return isinstance(node, nodes.TextElement)

        # sphinx.util.nodes.is_translatable() returns True for TextElement nodes unless node['translatable'] is False.
        for node in table_node.traverse(is_text_element):
            node['translatable'] = False

        return returned


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


class note(nodes.note, addnodes.translatable):
    ''' Named note as it needs to be a name that the sphinx builders know '''

    def preserve_original_messages(self):
        self['original_text'] = self.rawsource

    def apply_translated_message(self, original_message, translated_message):
        self.attributes['translation-found'] = True
        if translated_message.strip() == '-':
            self.attributes['ignore-note'] = True
        else:
            self.children = parse_markdown(translated_message)

    def extract_original_messages(self):
        return [self['original_text']]


class LocalizationNote(Note):

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = '\n'.join(self.content)
        self.options['localization_note'] = True
        admonition_node = note(text, **self.options)
        self.add_name(admonition_node)
        admonition_node.source, admonition_node.line = self.state.state_machine.get_source_and_line()
        # self.state.nested_parse(self.content, self.content_offset,
        #                         admonition_node)
        admonition_node.children = parse_markdown(text)
        return [admonition_node]


class RemoveLocalizationNote(Transform):
    """
    Remove localization note with a '-'.
    """
    default_priority = 21

    def apply(self):
        from sphinx.builders.gettext import MessageCatalogBuilder
        env = self.document.settings.env
        builder = env.app.builder
        if isinstance(builder, MessageCatalogBuilder):
            return
        for note in self.document.traverse(nodes.note):
            if 'localization_note' not in note.attributes:
                continue
            if (
                'ignore-note' in note.attributes or
                'translation-found' not in note.attributes or
                not env.config.language
            ):
                note.parent.remove(note)


def setup(app):

    if JSON_SUPPORT:
        from .json import (JSONInclude, JSONIncludeFlat, JSONIncludeQuote, JSONSchemaArrayDirective,
                           JSONSchemaTitleFieldnameMapDirective, JSONSchemaTitlesDirective)
        app.add_directive('jsoninclude', JSONInclude)
        app.add_directive('jsoninclude-flat', JSONIncludeFlat)
        app.add_directive('jsoninclude-quote', JSONIncludeQuote)
        app.add_directive('jsonschema-titles', JSONSchemaTitlesDirective)
        app.add_directive('jsonschema-title-fieldname-map', JSONSchemaTitleFieldnameMapDirective)
        app.add_directive('jsonschema-array', JSONSchemaArrayDirective)
    if MARKDOWN_SUPPORT:
        from .markdown import LiteralAndParsedMarkdownDirective, MarkdownDirective
        app.add_directive('markdown', MarkdownDirective)
        app.add_directive('literal-and-parsed-markdown', LiteralAndParsedMarkdownDirective)
    app.add_directive('csv-table-no-translate', CSVTableNoTranslate)
    app.add_directive('directory_list', DirectoryListDirective)
    app.add_directive('localization-note', LocalizationNote)

    app.add_transform(RemoveLocalizationNote)
