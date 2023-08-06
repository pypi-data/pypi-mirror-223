from typing import Optional
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import MarkdownLexer, get_lexer_by_name

def highlighter(code: str, lang: Optional[str] = None) -> str:
	if lang is None:
		lexer = MarkdownLexer()
	else:
		lexer = get_lexer_by_name(lang)
	formatter = HtmlFormatter()
	return highlight(code, lexer, formatter)


