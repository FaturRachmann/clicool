"""Backup manager for shell configuration files."""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from rich.console import Console

from .. import BACKUPS_DIR, CLICOOL_HOME

console = Console()


class BackupMetadata:
    """Metadata for a backup."""

    def __init__(
        self,
        backup_id: str,
        timestamp: str,
        shell: str,
        theme: Optional[str],
        files: list[str],
        checksum: str,
    ):
        self.backup_id = backup_id
        self.timestamp = timestamp
        self.shell = shell
        self.theme = theme
        self.files = files
        self.checksum = checksum

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            "backup_id": self.backup_id,
            "timestamp": self.timestamp,
            "shell": self.shell,
            "theme": self.theme,
            "files": self.files,
            "checksum": self.checksum,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "BackupMetadata":
        """Create from dictionary."""
        return cls(**data)


class BackupManager:
    """Manage backups of shell configuration files."""

    def __init__(self, max_backups: int = 10):
        """
        Initialize backup manager.

        Args:
            max_backups: Maximum number of backups to keep
        """
        self.max_backups = max_backups
        self.backups_dir = BACKUPS_DIR

        # Ensure backups directory exists
        self.backups_dir.mkdir(parents=True, exist_ok=True)

    def create_backup(
        self,
        config_path: Path,
        shell_type: str,
        theme_name: Optional[str] = None,
    ) -> Optional[BackupMetadata]:
        """
        Create a backup of a config file.

        Args:
            config_path: Path to config file to backup
            shell_type: Shell type (bash, zsh, fish)
            theme_name: Optional theme name

        Returns:
            BackupMetadata if successful, None otherwise
        """
        if not config_path.exists():
            console.print(
                f"[yellow]Config file doesn't exist: {config_path}[/yellow]"
            )
            return None

        # Generate backup ID and filename
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y%m%d_%H%M%S")
        backup_id = f"bkp_{timestamp_str}_{hashlib.md5(str(config_path).encode()).hexdigest()[:8]}"

        # Read original content
        try:
            with open(config_path, "r") as f:
                content = f.read()
        except Exception as e:
            console.print(f"[red]Error reading {config_path}: {e}[/red]")
            return None

        # Calculate checksum
        checksum = hashlib.sha256(content.encode()).hexdigest()

        # Create backup filename
        config_name = config_path.name.replace(".", "_")
        backup_filename = f"{config_name}_{timestamp_str}.bak"
        backup_path = self.backups_dir / backup_filename

        # Write backup
        try:
            with open(backup_path, "w") as f:
                f.write(content)
        except Exception as e:
            console.print(f"[red]Error writing backup: {e}[/red]")
            return None

        # Create metadata
        metadata = BackupMetadata(
            backup_id=backup_id,
            timestamp=timestamp.isoformat(),
            shell=shell_type,
            theme=theme_name,
            files=[str(config_path)],
            checksum=checksum,
        )

        # Save metadata
        self._save_metadata(backup_id, metadata)

        # Rotate old backups
        self._rotate_backups()

        console.print(
            f"[green]✓ Backup created: {backup_filename}[/green]"
        )

        return metadata

    def restore_backup(
        self,
        backup_id: str,
        config_path: Optional[Path] = None,
    ) -> bool:
        """
        Restore a backup.

        Args:
            backup_id: ID of backup to restore
            config_path: Optional path to restore to (default: original path)

        Returns:
            True if successful, False otherwise
        """
        # Load metadata
        metadata = self._load_metadata(backup_id)
        if not metadata:
            console.print(f"[red]Backup not found: {backup_id}[/red]")
            return False

        # Find backup file
        backup_file = self._find_backup_file(backup_id)
        if not backup_file:
            console.print(f"[red]Backup file not found for: {backup_id}[/red]")
            return False

        # Determine restore path
        if config_path is None:
            # Use original path from metadata
            if metadata.files:
                restore_path = Path(metadata.files[0])
            else:
                console.print("[red]Cannot determine restore path[/red]")
                return False
        else:
            restore_path = config_path

        # Read backup content
        try:
            with open(backup_file, "r") as f:
                content = f.read()
        except Exception as e:
            console.print(f"[red]Error reading backup: {e}[/red]")
            return False

        # Verify checksum
        current_checksum = hashlib.sha256(content.encode()).hexdigest()
        if current_checksum != metadata.checksum:
            console.print(
                "[yellow]Warning: Backup checksum mismatch[/yellow]"
            )

        # Write to restore path
        try:
            restore_path.parent.mkdir(parents=True, exist_ok=True)
            with open(restore_path, "w") as f:
                f.write(content)
            console.print(
                f"[green]✓ Restored backup {backup_id} to {restore_path}[/green]"
            )
            return True
        except Exception as e:
            console.print(f"[red]Error restoring backup: {e}[/red]")
            return False

    def list_backups(self) -> list[BackupMetadata]:
        """List all available backups."""
        backups = []

        if not self.backups_dir.exists():
            return backups

        # Find all metadata files
        for metadata_file in self.backups_dir.glob("*.json"):
            if metadata_file.name == "index.json":
                continue

            try:
                with open(metadata_file, "r") as f:
                    data = json.load(f)
                backups.append(BackupMetadata.from_dict(data))
            except Exception:
                continue

        # Sort by timestamp (newest first)
        backups.sort(key=lambda b: b.timestamp, reverse=True)

        return backups

    def delete_backup(self, backup_id: str) -> bool:
        """Delete a backup."""
        metadata = self._load_metadata(backup_id)
        if not metadata:
            return False

        # Delete backup file
        backup_file = self._find_backup_file(backup_id)
        if backup_file and backup_file.exists():
            backup_file.unlink()

        # Delete metadata file
        metadata_file = self.backups_dir / f"{backup_id}.json"
        if metadata_file.exists():
            metadata_file.unlink()

        console.print(f"[green]✓ Deleted backup {backup_id}[/green]")
        return True

    def clear_all_backups(self) -> int:
        """Clear all backups. Returns number of backups deleted."""
        count = 0
        backups = self.list_backups()

        for backup in backups:
            if self.delete_backup(backup.backup_id):
                count += 1

        return count

    def _save_metadata(self, backup_id: str, metadata: BackupMetadata) -> None:
        """Save backup metadata."""
        metadata_file = self.backups_dir / f"{backup_id}.json"
        with open(metadata_file, "w") as f:
            json.dump(metadata.to_dict(), f, indent=2)

    def _load_metadata(self, backup_id: str) -> Optional[BackupMetadata]:
        """Load backup metadata."""
        metadata_file = self.backups_dir / f"{backup_id}.json"
        if not metadata_file.exists():
            return None

        try:
            with open(metadata_file, "r") as f:
                data = json.load(f)
            return BackupMetadata.from_dict(data)
        except Exception:
            return None

    def _find_backup_file(self, backup_id: str) -> Optional[Path]:
        """Find backup file for a backup ID."""
        metadata = self._load_metadata(backup_id)
        if not metadata:
            return None

        # Extract filename from metadata
        if metadata.files:
            config_name = Path(metadata.files[0]).name.replace(".", "_")
            # Search for matching backup file
            for backup_file in self.backups_dir.glob(f"{config_name}_*.bak"):
                if backup_id in backup_file.name:
                    return backup_file

        return None

    def _rotate_backups(self) -> None:
        """Remove old backups beyond max_backups limit."""
        backups = self.list_backups()

        if len(backups) > self.max_backups:
            # Delete oldest backups
            for backup in backups[self.max_backups :]:
                self.delete_backup(backup.backup_id)

    def get_backup_content(self, backup_id: str) -> Optional[str]:
        """Get content of a backup file."""
        backup_file = self._find_backup_file(backup_id)
        if not backup_file or not backup_file.exists():
            return None

        try:
            with open(backup_file, "r") as f:
                return f.read()
        except Exception:
            return None


# Singleton instance
_manager = BackupManager()


def create_backup(
    config_path: Path, shell_type: str, theme_name: Optional[str] = None
) -> Optional[BackupMetadata]:
    """Create a backup."""
    return _manager.create_backup(config_path, shell_type, theme_name)


def restore_backup(backup_id: str, config_path: Optional[Path] = None) -> bool:
    """Restore a backup."""
    return _manager.restore_backup(backup_id, config_path)


def list_backups() -> list[BackupMetadata]:
    """List all backups."""
    return _manager.list_backups()


__all__ = [
    "BackupMetadata",
    "BackupManager",
    "create_backup",
    "restore_backup",
    "list_backups",
]
