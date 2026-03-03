"""
CLICOOL - Modern Terminal Theme & Profile Engine

Make your terminal look like it owns the system.
"""

__version__ = "0.1.5"
__author__ = "Trustlabs"

import os
from pathlib import Path

# Package root directory
PACKAGE_ROOT = Path(__file__).parent.parent

# Theme directories
THEMES_DIR = PACKAGE_ROOT / "themes"
BUILTIN_THEMES_DIR = THEMES_DIR / "builtin"
LAYERS_DIR = THEMES_DIR / "layers"
COMMUNITY_THEMES_DIR = THEMES_DIR / "community"

# Template directories
TEMPLATES_DIR = PACKAGE_ROOT / "templates"

# User config directory
HOME = Path.home()
CLICOOL_HOME = Path(os.environ.get("CLICOOL_HOME", HOME / ".clicool"))
BACKUPS_DIR = CLICOOL_HOME / "backups"
PROFILES_DIR = CLICOOL_HOME / "profiles"
CACHE_DIR = CLICOOL_HOME / "cache"

# Markers for injection
START_MARKER = "# >>> CLICOOL START: {theme} >>>"
END_MARKER = "# <<< CLICOOL END: {theme} <<<"

__all__ = [
    "__version__",
    "PACKAGE_ROOT",
    "THEMES_DIR",
    "BUILTIN_THEMES_DIR",
    "LAYERS_DIR",
    "COMMUNITY_THEMES_DIR",
    "TEMPLATES_DIR",
    "CLICOOL_HOME",
    "BACKUPS_DIR",
    "PROFILES_DIR",
    "CACHE_DIR",
    "START_MARKER",
    "END_MARKER",
]
