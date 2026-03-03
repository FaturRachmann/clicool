"""Banner animations for theme activation."""

import time
from rich.console import Console

console = Console()


class BannerAnimation:
    """Animate theme activation banners."""

    CLICOOL_BANNER = """
     ██████╗██╗   ██╗██╗     ██████╗ ██╗    ██╗
    ██╔════╝██║   ██║██║     ██╔══██╗██║    ██║
    ██║     ██║   ██║██║     ██████╔╝██║ █╗ ██║
    ██║     ██║   ██║██║     ██╔══██╗██║███╗██║
    ╚██████╗╚██████╔╝███████╗██████╔╝╚███╔███╔╝
     ╚═════╝ ╚═════╝ ╚══════╝╚═════╝  ╚══╝╚══╝
    """

    def __init__(self, style: str = "typewriter"):
        """
        Initialize animation.

        Args:
            style: Animation style (typewriter, fade-in, slide-in, glitch, matrix, none)
        """
        self.style = style

    def play(self, theme_name: str, theme_info: dict) -> None:
        """
        Play activation animation.

        Args:
            theme_name: Name of activated theme
            theme_info: Theme information dict
        """
        if self.style == "none":
            self._show_instant(theme_name, theme_info)
        elif self.style == "typewriter":
            self._show_typewriter(theme_name, theme_info)
        elif self.style == "fade-in":
            self._show_fade_in(theme_name, theme_info)
        elif self.style == "glitch":
            self._show_glitch(theme_name, theme_info)
        elif self.style == "matrix":
            self._show_matrix(theme_name, theme_info)
        else:
            self._show_instant(theme_name, theme_info)

    def _show_instant(self, theme_name: str, theme_info: dict) -> None:
        """Show instant banner (no animation)."""
        console.print(f"\n[bold cyan]{self.CLICOOL_BANNER}[/bold cyan]")
        console.print(f"\n[bold green]⚡ {theme_name} theme activated![/bold green]\n")

        self._show_details(theme_info)

    def _show_typewriter(self, theme_name: str, theme_info: dict) -> None:
        """Show typewriter animation."""
        # Show banner
        console.print(f"\n[bold cyan]{self.CLICOOL_BANNER}[/bold cyan]")

        # Type out activation message
        message = f"⚡ {theme_name} theme activated!"
        console.print()

        for char in message:
            console.print(char, end="", style="bold green")
            time.sleep(0.03)
        console.print()

        self._show_details(theme_info)

    def _show_fade_in(self, theme_name: str, theme_info: dict) -> None:
        """Show fade-in animation (simulated with brightness levels)."""
        console.print(f"\n[bold cyan]{self.CLICOOL_BANNER}[/bold cyan]")
        console.print()

        # Simulate fade with dim to bright
        message = f"⚡ {theme_name} theme activated!"
        for i in range(1, 4):
            if i == 1:
                console.print(f"\r[dim]{message}[/dim]    ", end="")
                time.sleep(0.1)
            elif i == 2:
                console.print(f"\r{message}    ", end="")
                time.sleep(0.1)
            else:
                console.print(f"\r[bold green]{message}[/bold green]    ")

        self._show_details(theme_info)

    def _show_glitch(self, theme_name: str, theme_info: dict) -> None:
        """Show glitch animation effect."""
        console.print(f"\n[bold cyan]{self.CLICOOL_BANNER}[/bold cyan]")
        console.print()

        # Glitch effect with random characters
        message = f"⚡ {theme_name} theme activated!"
        glitch_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"

        for _ in range(3):
            glitched = "".join(
                c if c == " " else glitch_chars[hash(c) % len(glitch_chars)]
                for c in message
            )
            console.print(f"\r[red]{glitched}[/red]    ", end="")
            time.sleep(0.05)

        console.print(f"\r[bold green]{message}[/bold green]    ")
        self._show_details(theme_info)

    def _show_matrix(self, theme_name: str, theme_info: dict) -> None:
        """Show matrix-style animation."""
        console.print(f"\n[bold cyan]{self.CLICOOL_BANNER}[/bold cyan]")
        console.print()

        # Matrix rain effect (simplified)
        message = f"⚡ {theme_name} theme activated!"
        console.print("[green]", end="")

        for i, char in enumerate(message):
            if i % 2 == 0:
                console.print("[bold green]" + char + "[/bold green]", end="")
            else:
                console.print("[dim green]" + char + "[/dim green]", end="")
            time.sleep(0.05)

        console.print("[/green]")
        self._show_details(theme_info)

    def _show_details(self, theme_info: dict) -> None:
        """Show theme details."""
        console.print("\n[dim]─────────────────────────────────────[/dim]")

        details = []
        if theme_info.get("version"):
            details.append(f"Version: {theme_info['version']}")
        if theme_info.get("author"):
            details.append(f"Author: {theme_info['author']}")
        if theme_info.get("widgets"):
            details.append(f"Widgets: {', '.join(theme_info['widgets'])}")
        if theme_info.get("layers"):
            details.append(f"Layers: {', '.join(theme_info['layers'])}")

        if details:
            console.print(" | ".join(details))
        else:
            console.print("Ready to use!")

        console.print("[dim]─────────────────────────────────────[/dim]\n")


__all__ = ["BannerAnimation"]
