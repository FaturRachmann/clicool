"""Config diff viewer for comparing shell configurations."""

import difflib
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from .backup import BackupManager

console = Console()


class ConfigDiffer:
    """Compare and display differences in configurations."""

    def __init__(self):
        self.backup_manager = BackupManager()

    def diff(
        self,
        config_path: Path,
        backup_id: str | None = None,
        original_content: str | None = None,
    ) -> str | None:
        """
        Show diff between current config and backup.

        Args:
            config_path: Path to current config file
            backup_id: Optional backup ID to compare against
            original_content: Optional original content to compare

        Returns:
            Diff string or None if comparison not possible
        """
        if not config_path.exists():
            console.print(f"[yellow]Config file not found: {config_path}[/yellow]")
            return None

        # Read current content
        try:
            with open(config_path) as f:
                current_content = f.read()
        except Exception as e:
            console.print(f"[red]Error reading {config_path}: {e}[/red]")
            return None

        # Get original content
        if backup_id:
            original_content = self.backup_manager.get_backup_content(backup_id)
            if not original_content:
                console.print(f"[red]Backup not found: {backup_id}[/red]")
                return None
        elif original_content is None:
            console.print("[yellow]No backup ID or original content provided[/yellow]")
            return None

        # Generate diff
        diff = self._generate_diff(
            original_content.splitlines(keepends=True),
            current_content.splitlines(keepends=True),
            "original",
            "current",
        )

        return diff

    def diff_themes(
        self,
        config_path: Path,
        theme1: str,
        theme2: str,
    ) -> str | None:
        """
        Show diff between two theme injections in a config.

        Args:
            config_path: Path to config file
            theme1: First theme name
            theme2: Second theme name

        Returns:
            Diff string or None
        """
        from ..core.injector import ConfigInjector

        injector = ConfigInjector()

        content1 = injector.extract_block(config_path, theme1)
        content2 = injector.extract_block(config_path, theme2)

        if not content1:
            console.print(f"[yellow]Theme '{theme1}' not found in config[/yellow]")
            return None

        if not content2:
            console.print(f"[yellow]Theme '{theme2}' not found in config[/yellow]")
            return None

        diff = self._generate_diff(
            content1.splitlines(keepends=True),
            content2.splitlines(keepends=True),
            theme1,
            theme2,
        )

        return diff

    def show_diff(
        self,
        config_path: Path,
        backup_id: str | None = None,
        original_content: str | None = None,
    ) -> None:
        """
        Display diff in terminal.

        Args:
            config_path: Path to current config file
            backup_id: Optional backup ID to compare against
            original_content: Optional original content to compare
        """
        diff = self.diff(config_path, backup_id, original_content)

        if diff:
            # Create syntax-highlighted diff
            syntax = Syntax(diff, "diff", theme="monokai", line_numbers=True)
            console.print(
                Panel(
                    syntax,
                    title="Config Diff",
                    border_style="blue",
                )
            )

    def _generate_diff(
        self,
        original: list[str],
        current: list[str],
        from_file: str,
        to_file: str,
    ) -> str:
        """Generate unified diff."""
        diff_lines = list(
            difflib.unified_diff(
                original,
                current,
                fromfile=from_file,
                tofile=to_file,
                n=3,
            )
        )

        return "".join(diff_lines)

    def get_changes_summary(
        self,
        config_path: Path,
        backup_id: str | None = None,
        original_content: str | None = None,
    ) -> dict:
        """
        Get summary of changes.

        Args:
            config_path: Path to current config file
            backup_id: Optional backup ID to compare against
            original_content: Optional original content to compare

        Returns:
            Dictionary with change statistics
        """
        if not config_path.exists():
            return {"added": 0, "removed": 0, "changed": 0}

        # Read current content
        try:
            with open(config_path) as f:
                current_content = f.read()
        except Exception:
            return {"added": 0, "removed": 0, "changed": 0}

        # Get original content
        if backup_id:
            original_content = self.backup_manager.get_backup_content(backup_id)
            if not original_content:
                return {"added": 0, "removed": 0, "changed": 0}
        elif original_content is None:
            return {"added": 0, "removed": 0, "changed": 0}

        # Calculate diff
        diff = list(
            difflib.unified_diff(
                original_content.splitlines(),
                current_content.splitlines(),
            )
        )

        added = 0
        removed = 0

        for line in diff:
            if line.startswith("+") and not line.startswith("+++"):
                added += 1
            elif line.startswith("-") and not line.startswith("---"):
                removed += 1

        return {
            "added": added,
            "removed": removed,
            "changed": added + removed,
        }

    def is_different(
        self,
        content1: str,
        content2: str,
    ) -> bool:
        """Check if two contents are different."""
        return content1.strip() != content2.strip()


# Singleton instance
_differ = ConfigDiffer()


def diff(
    config_path: Path,
    backup_id: str | None = None,
    original_content: str | None = None,
) -> str | None:
    """Get diff."""
    return _differ.diff(config_path, backup_id, original_content)


def show_diff(
    config_path: Path,
    backup_id: str | None = None,
    original_content: str | None = None,
) -> None:
    """Show diff in terminal."""
    _differ.show_diff(config_path, backup_id, original_content)


__all__ = [
    "ConfigDiffer",
    "diff",
    "show_diff",
]
