from markdown_it import MarkdownIt
from markdown_it.renderer import RendererHTML
from markdown_it.rules_block import StateBlock
from .pygments import highlighter

class MarkdownItHighlighter(MarkdownIt):
	def __init__(self, *args, **kwargs):
		super().__init__(
				"commonmark",
				options_update={
					"html": True,
					"typographer": True,
					"highlight": highlighter,
				}
			)

markdownit = MarkdownItHighlighter()

def render_markdown(text: str) -> str:
	return markdownit.render(text)