"""CLICOOL CLI - Modern Terminal Theme & Profile Engine."""

from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel

from . import CLICOOL_HOME, __version__
from .config import ClicoolConfig
from .core.injector import ConfigInjector
from .core.shell import ShellDetector, ShellType
from .core.terminal import TerminalProbe
from .core.theme_loader import ThemeLoader, list_layers, list_themes
from .features.animations import BannerAnimation
from .features.doctor import run_doctor
from .safety.backup import BackupManager, create_backup

# Initialize Typer app
app = typer.Typer(
    name="clicool",
    help="Modern Terminal Theme & Profile Engine",
    add_completion=True,
)

console = Console()

# Initialize components
shell_detector = ShellDetector()
terminal_probe = TerminalProbe()
theme_loader = ThemeLoader()
backup_manager = BackupManager()
config = ClicoolConfig.load()


@app.callback(invoke_without_command=True)
def main_callback(
    version: bool = typer.Option(
        False,
        "--version",
        "-v",
        help="Show version and exit.",
    ),
):
    """CLICOOL - Make your terminal look like it owns the system."""
    if version:
        console.print(f"[bold cyan]clicool[/bold cyan] version [green]{__version__}[/green]")
        raise typer.Exit()


@app.command()
def init():
    """Initialize clicool configuration."""
    config.ensure_config_dir()
    config.save()
    console.print("[green]✓ clicool initialized successfully![/green]")
    console.print(f"[dim]Config directory: {CLICOOL_HOME}[/dim]")


@app.command()
def enable(
    theme_name: str = typer.Argument(..., help="Theme name to enable"),
    preview: bool = typer.Option(False, "--preview", "-p", help="Preview theme before applying"),
    dry_run: bool = typer.Option(False, "--dry-run", "-n", help="Show what would be changed"),
    layer: list[str] | None = typer.Option(None, "--layer", "-l", help="Add layer to theme"),
    random: bool = typer.Option(False, "--random", "-r", help="Enable random theme"),
):
    """
    Enable a theme.

    Example: clicool enable cyberpunk
    """
    import random as random_module

    # Handle random theme
    if random:
        available_themes = list_themes()
        if not available_themes:
            console.print("[red]No themes available[/red]")
            raise typer.Exit(1)
        theme_name = random_module.choice(available_themes)
        console.print(f"[dim]Random theme selected: {theme_name}[/dim]")

    # Ensure config directory exists
    config.ensure_config_dir()

    # Detect shell
    shell_info = shell_detector.detect()
    if shell_info.shell_type == ShellType.UNKNOWN:
        console.print("[yellow]Warning: Could not detect shell type[/yellow]")
        shell_type = "bash"
    else:
        shell_type = shell_info.shell_type.value

    # Get config path
    config_path = shell_info.config_path

    # Load theme
    try:
        theme = theme_loader.load_theme(theme_name)
    except FileNotFoundError:
        console.print(f"[red]Theme '{theme_name}' not found[/red]")
        console.print(f"[dim]Available themes: {', '.join(list_themes())}[/dim]")
        raise typer.Exit(1)

    # Preview mode
    if preview:
        preview_theme(theme_name, theme)
        if not typer.confirm("Apply this theme?"):
            raise typer.Exit(0)

    # Dry run mode
    if dry_run or config.dry_run:
        console.print(f"[yellow]Dry run: Would enable theme '{theme_name}'[/yellow]")
        console.print(f"[dim]Shell: {shell_type}[/dim]")
        console.print(f"[dim]Config: {config_path}[/dim]")
        raise typer.Exit(0)

    # Create backup
    if config.auto_backup and config_path.exists():
        create_backup(config_path, shell_type, theme_name)

    # Generate config
    from .core.generator import AdvancedPromptGenerator

    generator = AdvancedPromptGenerator()

    # Load layers if specified
    layers = []
    if layer:
        from .core.theme_loader import load_layer

        for layer_name in layer:
            try:
                layers.append(load_layer(layer_name))
            except FileNotFoundError:
                console.print(f"[yellow]Layer '{layer_name}' not found, skipping[/yellow]")

    # Generate theme config
    theme_config = generator.generate(theme, shell_type, layers)

    # Inject config
    injector = ConfigInjector(dry_run=False)
    success, message = injector.inject(config_path, theme_config, theme_name)

    console.print(message)

    if success:
        # Update config
        config.active_theme = theme_name
        config.active_layers = layer or []
        config.save()

        # Show activation banner
        if config.enable_animations:
            banner = BannerAnimation(style=config.animation_style)
            banner.play(theme.name, theme_loader.get_theme_info(theme_name))
        else:
            console.print(f"[green]✓ Theme '{theme_name}' enabled![/green]")

        # Show reload instructions
        console.print()
        console.print(
            Panel(
                f"[bold]To see your new theme:[/bold]\n\n"
                f"  [cyan]source {config_path}[/cyan]\n\n"
                f"[dim]Or restart your terminal[/dim]",
                title="🎨 Theme Applied!",
                border_style="green",
            )
        )

        # Show quick test
        console.print()
        console.print(
            "[dim]💡 Quick test: Run 'clicool preview cyberpunk' to see theme preview[/dim]"
        )


@app.command()
def disable(
    rollback: bool = typer.Option(False, "--rollback", "-r", help="Rollback to previous backup"),
):
    """Disable current theme."""
    config.ensure_config_dir()

    if not config.active_theme:
        console.print("[yellow]No active theme to disable[/yellow]")
        raise typer.Exit(0)

    shell_info = shell_detector.detect()
    config_path = shell_info.config_path

    # Remove theme injection
    injector = ConfigInjector()
    success, message = injector.remove(config_path, config.active_theme)
    console.print(message)

    if success:
        config.active_theme = None
        config.active_layers = []
        config.save()
        console.print(f"[green]✓ Theme '{config.active_theme}' disabled![/green]")


@app.command()
def list(
    installed: bool = typer.Option(False, "--installed", "-i", help="Show only installed themes"),
    remote: bool = typer.Option(False, "--remote", "-r", help="Browse remote themes"),
    layers: bool = typer.Option(False, "--layers", "-l", help="Show available layers"),
):
    """List available themes."""
    if layers:
        available_layers = list_layers()
        if not available_layers:
            console.print("[yellow]No layers available[/yellow]")
        else:
            console.print("[bold]Available Layers:[/bold]")
            for layer in available_layers:
                console.print(f"  • {layer}")
        return

    if remote:
        console.print("[yellow]Remote theme marketplace coming soon...[/yellow]")
        return

    available_themes = list_themes()

    if not available_themes:
        console.print("[yellow]No themes available[/yellow]")
        console.print("[dim]Themes should be in themes/builtin/ directory[/dim]")
        return

    console.print("[bold]Available Themes:[/bold]")
    for theme in available_themes:
        is_active = theme == config.active_theme
        marker = "[green]●[/green] " if is_active else "  "
        info = theme_loader.get_theme_info(theme)
        description = info.get("description", "")[:50]
        console.print(f"{marker}[cyan]{theme}[/cyan] - [dim]{description}[/dim]")


@app.command()
def preview(theme_name: str = typer.Argument(..., help="Theme name to preview")):
    """Preview a theme without applying it."""
    try:
        theme = theme_loader.load_theme(theme_name)
    except FileNotFoundError:
        console.print(f"[red]Theme '{theme_name}' not found[/red]")
        raise typer.Exit(1)

    preview_theme(theme_name, theme)


def preview_theme(theme_name: str, theme):
    """Show theme preview."""

    console.print(f"\n[bold cyan]═══ Theme Preview: {theme_name} ═══[/bold cyan]\n")

    # Show prompt example with actual colors
    console.print("[bold]Example Prompt:[/bold]")

    # Get colors

    # Display colored prompt example (clean, no emojis)
    console.print(
        "\033[1;96mdev\033[0m@"
        "\033[1;95mmachine\033[0m:"
        "\033[1;93m~/projects/clicool\033[0m"
        "\033[2m(\033[1;92mmain\033[2m)\033[0m"
    )
    console.print("\033[1;92m>\033[0m ")

    console.print()

    # Show theme info
    console.print("[bold]Theme Details:[/bold]")
    console.print(f"  • Name: {theme.name}")
    console.print(f"  • Version: {theme.version}")
    if theme.description:
        console.print(f"  • Description: {theme.description}")
    if theme.tags:
        console.print(f"  • Tags: {', '.join(theme.tags)}")

    # Show features
    if theme.features:
        console.print("\n[bold]Features:[/bold]")
        features = theme.features.model_dump() if hasattr(theme.features, "model_dump") else {}
        for key, value in features.items():
            if isinstance(value, bool):
                status = "✓" if value else "✗"
                console.print(f"  {status} {key.replace('_', ' ').title()}")

    # Show widgets
    if theme.widgets:
        console.print(f"\n[bold]Widgets:[/bold] {', '.join(theme.widgets)}")

    # Show layers
    if theme.layers:
        console.print(f"\n[bold]Layers:[/bold] {', '.join(theme.layers)}")

    console.print()


@app.command()
def doctor(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Show detailed output"),
    fix: bool = typer.Option(False, "--fix", "-f", help="Auto-fix issues"),
):
    """Check environment for issues."""
    run_doctor(verbose=verbose, auto_fix=fix)


@app.command()
def backup(
    list_backups_flag: bool = typer.Option(False, "--list", "-l", help="List backups"),
):
    """Create or manage backups."""
    if list_backups_flag:
        backups = backup_manager.list_backups()
        if not backups:
            console.print("[yellow]No backups found[/yellow]")
        else:
            console.print("[bold]Available Backups:[/bold]")
            for backup in backups:
                console.print(f"  • {backup.backup_id} - {backup.timestamp} ({backup.shell})")
        return

    # Create backup
    shell_info = shell_detector.detect()
    config_path = shell_info.config_path

    if not config_path.exists():
        console.print(f"[yellow]Config file not found: {config_path}[/yellow]")
        raise typer.Exit(1)

    create_backup(config_path, shell_info.shell_type.value)


@app.command()
def restore(
    backup_id: str = typer.Argument(None, help="Backup ID to restore"),
    list_backups_flag: bool = typer.Option(False, "--list", "-l", help="List backups"),
):
    """Restore from backup."""
    if list_backups_flag or not backup_id:
        backups = backup_manager.list_backups()
        if not backups:
            console.print("[yellow]No backups found[/yellow]")
        else:
            console.print("[bold]Available Backups:[/bold]")
            for backup in backups:
                console.print(f"  • {backup.backup_id} - {backup.timestamp} ({backup.shell})")
        return

    shell_info = shell_detector.detect()
    config_path = shell_info.config_path

    success = backup_manager.restore_backup(backup_id, config_path)
    if not success:
        raise typer.Exit(1)


@app.command()
def diff():
    """Show config changes."""
    from .safety.diff import show_diff

    shell_info = shell_detector.detect()
    config_path = shell_info.config_path

    if not config_path.exists():
        console.print(f"[yellow]Config file not found: {config_path}[/yellow]")
        raise typer.Exit(1)

    show_diff(config_path)


@app.command()
def status():
    """Show current theme status."""
    if not config.active_theme:
        console.print("[yellow]No theme currently active[/yellow]")
        return

    console.print(f"[bold]Active Theme:[/bold] {config.active_theme}")
    console.print(f"[bold]Version:[/bold] {__version__}")

    if config.active_layers:
        console.print(f"[bold]Layers:[/bold] {', '.join(config.active_layers)}")

    shell_info = shell_detector.detect()
    console.print(f"[bold]Shell:[/bold] {shell_info.shell_type.value}")
    console.print(f"[bold]Config:[/bold] {shell_info.config_path}")


@app.command()
def search(query: str = typer.Argument(..., help="Search query")):
    """Search for themes."""
    available_themes = list_themes()
    matches = [t for t in available_themes if query.lower() in t.lower()]

    if not matches:
        console.print(f"[yellow]No themes matching '{query}'[/yellow]")
        return

    console.print(f"[bold]Found {len(matches)} theme(s):[/bold]")
    for theme in matches:
        info = theme_loader.get_theme_info(theme)
        description = info.get("description", "")[:50]
        console.print(f"  • [cyan]{theme}[/cyan] - [dim]{description}[/dim]")


@app.command()
def theme(
    action: str = typer.Argument("list", help="Action: new, validate, package, publish"),
    name: str | None = typer.Argument(None, help="Theme name"),
):
    """Manage themes."""
    if action == "validate" and name:
        from .core.validator import validate_file

        theme_path = Path(name)
        if not theme_path.exists():
            # Try builtin themes
            theme_path = theme_loader.BUILTIN_THEMES_DIR / f"{name}.json"

        if not theme_path.exists():
            console.print(f"[red]Theme file not found: {name}[/red]")
            raise typer.Exit(1)

        result = validate_file(theme_path)
        if result:
            console.print("[green]✓ Theme is valid[/green]")
        else:
            console.print("[red]✗ Theme is invalid:[/red]")
            for error in result.errors:
                console.print(f"  • {error}")
            raise typer.Exit(1)
    elif action == "list":
        list()
    else:
        console.print(f"[yellow]Action '{action}' not implemented yet[/yellow]")


@app.command()
def demo():
    """Show theme demo with color bars."""
    console.print("\n[bold cyan]═══ CLICOOL Theme Demo ═══[/bold cyan]\n")

    # Show color palette for each theme
    themes_info = [
        ("cyberpunk", "Cyberpunk", "#00ffff", "#ff00ff", "#ffff00", "#00ff00"),
        ("matrix", "Matrix", "#00ff00", "#00cc00", "#008800", "#00ff00"),
        ("retro", "Retro", "#ffb000", "#ff9900", "#cc8800", "#ffb000"),
        ("devops", "DevOps", "#00d9ff", "#ff9900", "#00ff99", "#ff66cc"),
    ]

    for _theme_key, theme_name, c1, c2, c3, c4 in themes_info:
        console.print(f"[bold]{theme_name}:[/bold]")
        # Show color bar
        console.print(f"[{c1}]████[/{c1}][{c2}]████[/{c2}][{c3}]████[/{c3}][{c4}]████[/{c4}]")
        console.print()

    console.print("[dim]Run 'clicool enable <theme>' to apply a theme[/dim]")
    console.print("[dim]Then run 'source ~/.bashrc' to see changes[/dim]\n")


@app.command()
def profile(
    action: str = typer.Argument("list", help="Action: save, load, list, delete, export, import"),
    name: str | None = typer.Argument(None, help="Profile name"),
):
    """Manage profiles."""
    if action == "list" or not name:
        console.print("[yellow]Profile management coming soon...[/yellow]")
    elif action == "save":
        console.print(f"[yellow]Saving profile '{name}'...[/yellow]")
        config.active_theme = name
        config.save()
        console.print(f"[green]✓ Profile '{name}' saved[/green]")
    elif action == "load":
        console.print(f"[yellow]Loading profile '{name}'...[/yellow]")
        console.print("[yellow]Profile loading coming soon...[/yellow]")
    else:
        console.print(f"[yellow]Action '{action}' not implemented yet[/yellow]")


@app.command()
def plugin(
    action: str = typer.Argument("list", help="Action: install, list, enable, disable"),
    name: str | None = typer.Argument(None, help="Plugin name"),
):
    """Manage plugins."""
    console.print("[yellow]Plugin management coming soon...[/yellow]")


@app.command()
def cache(
    action: str = typer.Argument("clear", help="Action: clear"),
):
    """Manage cache."""
    from . import CACHE_DIR

    if action == "clear":
        if CACHE_DIR.exists():
            import shutil

            shutil.rmtree(CACHE_DIR)
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
            console.print("[green]✓ Cache cleared[/green]")
        else:
            console.print("[dim]Cache directory doesn't exist[/dim]")


def cli():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    cli()
