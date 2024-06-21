from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.utils import new_document

try:
    from myst_parser.main import to_docutils
except ModuleNotFoundError:
    from myst_parser.config.main import MdParserConfig
    from myst_parser.mdit_to_docutils.base import make_document
    from myst_parser.mdit_to_docutils.sphinx_ import SphinxRenderer
    from myst_parser.parsers.mdit import create_md_parser

    # to_docutils was removed in myst-parser>=0.18.
    def to_docutils(text, document=None):
        # Code is similar to MystParser.parse and myst_parser.parsers.docutils_.Parser.parse.
        parser = create_md_parser(MdParserConfig(), SphinxRenderer)
        if not document:
            document = make_document()
        parser.options["document"] = document
        return parser.render(text)


def parse_markdown(text, document=None):
    if document:
        document = new_document(None, document.settings)
    return to_docutils(text, document=document).children[:]


class MarkdownDirective(Directive):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return parse_markdown(text, document=self.state.document)


class LiteralAndParsedMarkdownDirective(Directive):
    has_content = True

    def run(self):
        text = '\n'.join(self.content)
        return [
            nodes.paragraph('', '', nodes.Text('Source:')),
            nodes.literal_block(text, text),
            nodes.paragraph('', '', nodes.Text('Output:')),
        ] + parse_markdown(text, document=self.state.document)
