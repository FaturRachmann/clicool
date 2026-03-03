"""Theme preview renderer."""

from rich.console import Console
from rich.panel import Panel

console = Console()


class ThemePreview:
    """Preview theme appearance."""

    def show_preview(self, theme_name: str, theme_config: dict) -> None:
        """
        Show theme preview.

        Args:
            theme_name: Name of theme
            theme_config: Theme configuration dict
        """
        console.print(f"\n[bold cyan]Preview: {theme_name}[/bold cyan]\n")

        # Show prompt example
        prompt_example = self._generate_prompt_example(theme_config)
        console.print(Panel(prompt_example, title="Prompt Example", border_style="cyan"))

        # Show colors
        if theme_config.get("prompt", {}).get("colors"):
            colors = theme_config["prompt"]["colors"]
            self._show_colors(colors)

        # Show features
        if theme_config.get("features"):
            features = theme_config["features"]
            self._show_features(features)

    def _generate_prompt_example(self, theme_config: dict) -> str:
        """Generate prompt example string."""
        # Default example
        user = "dev"
        host = "machine"
        path = "~/projects/clicool"
        branch = "main"

        template = theme_config.get("prompt", {}).get("template")
        if template:
            example = template.format(
                user=user,
                host=host,
                path=path,
                git_branch=f" ({branch})",
            )
        else:
            example = f"{user}@{host}:{path} ({branch}) λ"

        return example

    def _show_colors(self, colors: dict) -> None:
        """Show color palette."""
        console.print("\n[bold]Colors:[/bold]")
        for name, color in colors.items():
            if color:
                console.print(f"  [{color}]{name}: {color}[/{color}]")

    def _show_features(self, features: dict) -> None:
        """Show enabled features."""
        console.print("\n[bold]Features:[/bold]")
        for key, value in features.items():
            if isinstance(value, bool):
                status = "✓" if value else "✗"
                console.print(f"  {status} {key.replace('_', ' ').title()}")


__all__ = ["ThemePreview"]
