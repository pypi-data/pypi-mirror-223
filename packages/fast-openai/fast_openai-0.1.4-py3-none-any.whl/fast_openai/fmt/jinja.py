from functools import wraps
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
from jinja2.exceptions import (TemplateAssertionError, TemplateError,
                               TemplateNotFound, TemplateSyntaxError,
                               UndefinedError)
from fastapi.responses import HTMLResponse
from fastapi import Request, APIRouter
from .markdownit import render_markdown
from ..utils import setup_logging

logger = setup_logging(__name__)

def handle_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (TemplateNotFound, UndefinedError, TemplateAssertionError, TemplateError, TemplateSyntaxError) as e:
            logger.error(e.__class__.__name__)
            logger.error(e)
            return HTMLResponse(str(e), status_code=500)
    return wrapper

class TemplateResponse(HTMLResponse):
    template: Template
    context: dict

    def __init__(self, template: Template, context: dict = {}, status_code: int = 200):
        self.template = template
        self.context = context
        super().__init__(self.template.render(**self.context), status_code=status_code)

class MarkdownResponse(HTMLResponse):
    def __init__(self, markdown: str, status_code: int = 200):
        self.template = markdown
        super().__init__(render_markdown(markdown), status_code=status_code)        

class MarkdownTemplate(HTMLResponse):
    def __init__(self, template: Template, context: dict = {}, status_code: int = 200):
        self.template =template
        self.context = context
        self.status_code = status_code
        super().__init__(render_markdown(self.template.render(**self.context)), status_code=status_code)

class SSRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix="/"
        self.tags = ["SSRouter"]
        self.include_in_schema = False
        self.env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(["html", "xml", "md"]),
        )
        self.env.filters["md"] = render_markdown

    @handle_errors
    def template(self, template_name: str, **kwargs) -> TemplateResponse:
        template = self.env.get_template(template_name)
        return TemplateResponse(template, context=kwargs)

    @handle_errors
    def markdown(self, markdown: str, **kwargs) -> MarkdownResponse:
        return MarkdownResponse(markdown, **kwargs)

    @handle_errors
    def markdown_template(self, template_name: str, **kwargs) -> MarkdownTemplate:
        template = self.env.get_template(template_name)
        return MarkdownTemplate(template, context=kwargs)