"""Template engine utilities."""

from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .. import TEMPLATES_DIR


class TemplateEngine:
    """Jinja2 template engine for clicool."""

    def __init__(self, template_dir: Path | None = None):
        """
        Initialize template engine.

        Args:
            template_dir: Optional custom template directory
        """
        if template_dir is None:
            template_dir = TEMPLATES_DIR

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Register custom filters
        self._register_filters()

    def _register_filters(self) -> None:
        """Register custom Jinja2 filters."""

        @self.env.filter
        def upper(value: str) -> str:
            return value.upper() if value else ""

        @self.env.filter
        def lower(value: str) -> str:
            return value.lower() if value else ""

        @self.env.filter
        def replace(value: str, old: str, new: str) -> str:
            return value.replace(old, new) if value else ""

    def render(
        self,
        template_name: str,
        context: dict[str, Any],
    ) -> str:
        """
        Render a template.

        Args:
            template_name: Name of template file
            context: Template context variables

        Returns:
            Rendered template string
        """
        template = self.env.get_template(template_name)
        return str(template.render(**context))  # type: ignore

    def render_string(
        self,
        template_string: str,
        context: dict[str, Any],
    ) -> str:
        """
        Render a template string.

        Args:
            template_string: Template string
            context: Template context variables

        Returns:
            Rendered string
        """
        template = self.env.from_string(template_string)
        return str(template.render(**context))  # type: ignore

    def template_exists(self, template_name: str) -> bool:
        """
        Check if template exists.

        Args:
            template_name: Name of template

        Returns:
            True if template exists
        """
        return bool(self.env.loader.has_source(self.env, template_name))  # type: ignore


# Default template variables
DEFAULT_CONTEXT = {
    "version": "0.1.0",
    "author": "clicool",
    "homepage": "https://github.com/clicool/clicool",
}


def render_template(
    template_name: str,
    context: dict[str, Any] | None = None,
) -> str:
    """
    Render a template.

    Args:
        template_name: Name of template file
        context: Template context variables

    Returns:
        Rendered template string
    """
    engine = TemplateEngine()
    ctx = {**DEFAULT_CONTEXT, **(context or {})}
    return engine.render(template_name, ctx)


def render_template_string(
    template_string: str,
    context: dict[str, Any] | None = None,
) -> str:
    """
    Render a template string.

    Args:
        template_string: Template string
        context: Template context variables

    Returns:
        Rendered string
    """
    engine = TemplateEngine()
    ctx = {**DEFAULT_CONTEXT, **(context or {})}
    return engine.render_string(template_string, ctx)


__all__ = [
    "TemplateEngine",
    "render_template",
    "render_template_string",
]
