"""Global configuration management for clicool."""

import json
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field

# Import paths from package
from . import BACKUPS_DIR, CACHE_DIR, CLICOOL_HOME, PROFILES_DIR


class ClicoolConfig(BaseModel):
    """Configuration model for clicool."""

    # Current active theme
    active_theme: Optional[str] = None
    # Active layers
    active_layers: list[str] = Field(default_factory=list)
    # Active widgets
    active_widgets: list[str] = Field(default_factory=list)
    # Shell config file path
    shell_config_path: Optional[str] = None
    # Auto backup on enable
    auto_backup: bool = True
    # Enable animations
    enable_animations: bool = True
    # Animation style
    animation_style: str = "typewriter"
    # Dry run mode (global)
    dry_run: bool = False
    # Verbose output
    verbose: bool = False
    # Check for updates
    check_updates: bool = True
    # Theme marketplace URL
    marketplace_url: str = "https://clicool.dev/api/themes"
    # Max backups to keep
    max_backups: int = 10
    # Custom template variables
    custom_variables: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "ClicoolConfig":
        """Load configuration from file."""
        if config_path is None:
            config_path = CLICOOL_HOME / "config.json"

        if not config_path.exists():
            return cls()

        try:
            with open(config_path, "r") as f:
                data = json.load(f)
            return cls(**data)
        except (json.JSONDecodeError, Exception) as e:
            # Return default config on error
            return cls()

    def save(self, config_path: Optional[Path] = None) -> None:
        """Save configuration to file."""
        if config_path is None:
            config_path = CLICOOL_HOME / "config.json"

        # Ensure directory exists
        config_path.parent.mkdir(parents=True, exist_ok=True)

        with open(config_path, "w") as f:
            json.dump(self.model_dump(), f, indent=2)

    def ensure_config_dir(self) -> None:
        """Ensure clicool config directory exists."""
        CLICOOL_HOME.mkdir(parents=True, exist_ok=True)
        BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
        PROFILES_DIR.mkdir(parents=True, exist_ok=True)
        CACHE_DIR.mkdir(parents=True, exist_ok=True)


# Config file path
CONFIG_FILE = CLICOOL_HOME / "config.json"

__all__ = ["ClicoolConfig", "CONFIG_FILE"]
