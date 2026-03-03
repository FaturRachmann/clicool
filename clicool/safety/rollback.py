"""Rollback engine for reverting theme changes."""

from pathlib import Path
from typing import Optional, Tuple

from rich.console import Console

from .backup import BackupManager, BackupMetadata, list_backups

console = Console()


class RollbackEngine:
    """Engine for rolling back theme changes."""

    def __init__(self):
        self.backup_manager = BackupManager()

    def rollback(
        self,
        config_path: Path,
        theme_name: Optional[str] = None,
        backup_id: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """
        Rollback theme changes.

        Args:
            config_path: Path to shell config file
            theme_name: Optional theme name to rollback
            backup_id: Optional specific backup ID to restore

        Returns:
            Tuple of (success, message)
        """
        if backup_id:
            # Restore specific backup
            return self._restore_specific_backup(backup_id, config_path)
        elif theme_name:
            # Rollback specific theme
            return self._rollback_theme(theme_name, config_path)
        else:
            # Rollback to latest backup
            return self._rollback_to_latest(config_path)

    def _restore_specific_backup(
        self, backup_id: str, config_path: Path
    ) -> Tuple[bool, str]:
        """Restore a specific backup."""
        metadata = self._get_backup_metadata(backup_id)
        if not metadata:
            return (False, f"[red]Backup not found: {backup_id}[/red]")

        success = self.backup_manager.restore_backup(backup_id, config_path)
        if success:
            return (
                True,
                f"[green]✓ Restored backup {backup_id}[/green]",
            )
        else:
            return (
                False,
                f"[red]Failed to restore backup {backup_id}[/red]",
            )

    def _rollback_theme(
        self, theme_name: str, config_path: Path
    ) -> Tuple[bool, str]:
        """Rollback a specific theme."""
        # Find backup for this theme
        backups = self.backup_manager.list_backups()
        theme_backup = None

        for backup in backups:
            if backup.theme == theme_name:
                theme_backup = backup
                break

        if not theme_backup:
            return (
                False,
                f"[yellow]No backup found for theme '{theme_name}'[/yellow]",
            )

        success = self.backup_manager.restore_backup(
            theme_backup.backup_id, config_path
        )
        if success:
            return (
                True,
                f"[green]✓ Rolled back theme '{theme_name}'[/green]",
            )
        else:
            return (
                False,
                f"[red]Failed to rollback theme '{theme_name}'[/red]",
            )

    def _rollback_to_latest(self, config_path: Path) -> Tuple[bool, str]:
        """Rollback to latest backup."""
        backups = self.backup_manager.list_backups()

        if not backups:
            return (
                False,
                "[yellow]No backups available for rollback[/yellow]",
            )

        latest_backup = backups[0]
        success = self.backup_manager.restore_backup(
            latest_backup.backup_id, config_path
        )
        if success:
            return (
                True,
                f"[green]✓ Rolled back to latest backup ({latest_backup.backup_id})[/green]",
            )
        else:
            return (
                False,
                f"[red]Failed to rollback to latest backup[/red]",
            )

    def _get_backup_metadata(self, backup_id: str) -> Optional[BackupMetadata]:
        """Get metadata for a backup."""
        backups = self.backup_manager.list_backups()
        for backup in backups:
            if backup.backup_id == backup_id:
                return backup
        return None

    def get_rollback_options(self, config_path: Path) -> list[dict]:
        """
        Get available rollback options.

        Args:
            config_path: Path to shell config file

        Returns:
            List of rollback options with metadata
        """
        backups = self.backup_manager.list_backups()
        options = []

        for backup in backups:
            options.append(
                {
                    "backup_id": backup.backup_id,
                    "timestamp": backup.timestamp,
                    "shell": backup.shell,
                    "theme": backup.theme,
                    "files": backup.files,
                }
            )

        return options

    def can_rollback(self, config_path: Path) -> bool:
        """Check if rollback is possible."""
        backups = self.backup_manager.list_backups()
        return len(backups) > 0


# Singleton instance
_engine = RollbackEngine()


def rollback(
    config_path: Path,
    theme_name: Optional[str] = None,
    backup_id: Optional[str] = None,
) -> Tuple[bool, str]:
    """Perform rollback."""
    return _engine.rollback(config_path, theme_name, backup_id)


def get_rollback_options(config_path: Path) -> list[dict]:
    """Get rollback options."""
    return _engine.get_rollback_options(config_path)


__all__ = [
    "RollbackEngine",
    "rollback",
    "get_rollback_options",
]
