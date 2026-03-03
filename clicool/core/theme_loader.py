"""Theme loader and parser for clicool theme JSON files."""

import json
from pathlib import Path
from typing import Optional, Union

from pydantic import BaseModel, Field, field_validator

from .. import BUILTIN_THEMES_DIR, COMMUNITY_THEMES_DIR, LAYERS_DIR


class ColorConfig(BaseModel):
    """Color configuration for theme elements."""

    user: Optional[str] = None
    host: Optional[str] = None
    path: Optional[str] = None
    git_branch: Optional[str] = None
    symbol: Optional[str] = None
    # Additional colors
    background: Optional[str] = None
    foreground: Optional[str] = None
    cursor: Optional[str] = None
    selection: Optional[str] = None


class IconConfig(BaseModel):
    """Icon configuration for theme elements."""

    user: Optional[str] = None
    git: Optional[str] = None
    error: Optional[str] = None
    # Additional icons
    success: Optional[str] = None
    warning: Optional[str] = None
    info: Optional[str] = None


class PromptConfig(BaseModel):
    """Prompt configuration."""

    format: str = "default"
    template: Optional[str] = None
    colors: Optional[ColorConfig] = None
    icons: Optional[IconConfig] = None


class FeaturesConfig(BaseModel):
    """Features configuration."""

    show_git: bool = True
    show_time: bool = True
    time_format: str = "%H:%M:%S"
    show_exit_code: bool = True
    show_user: bool = True
    show_host: bool = True
    shorten_path: bool = True
    path_depth: int = 3
    show_k8s: bool = False
    show_docker: bool = False
    show_aws: bool = False


class TerminalColorPalette(BaseModel):
    """Terminal color palette configuration."""

    background: Optional[str] = None
    foreground: Optional[str] = None
    cursor: Optional[str] = None
    selection: Optional[str] = None
    ansi: Optional[list[str]] = None


class TerminalConfig(BaseModel):
    """Terminal configuration."""

    color_palette: Optional[TerminalColorPalette] = None
    font_recommendation: Optional[str] = None
    opacity: Optional[float] = Field(default=None, ge=0.0, le=1.0)


class BannerConfig(BaseModel):
    """Banner configuration."""

    enabled: bool = True
    style: str = "default"
    animation: str = "none"


class WidgetConfig(BaseModel):
    """Widget configuration."""

    name: str
    position: str = "prompt-suffix"
    priority: int = 100
    config: dict = Field(default_factory=dict)


class LayerConfig(BaseModel):
    """Layer configuration for modular themes."""

    name: str
    type: str = "layer"
    version: str = "1.0.0"
    widget: Optional[WidgetConfig] = None


class ThemeConfig(BaseModel):
    """Main theme configuration model."""

    schema_url: Optional[str] = Field(default=None, alias="$schema")
    name: str
    version: str = "1.0.0"
    author: Optional[str] = None
    description: Optional[str] = None
    tags: list[str] = Field(default_factory=list)
    type: str = "theme"  # "theme" or "layer"

    # Prompt configuration
    prompt: Optional[PromptConfig] = None

    # Features
    features: Optional[FeaturesConfig] = None

    # Terminal configuration
    terminal: Optional[TerminalConfig] = None

    # Widgets and layers
    widgets: list[str] = Field(default_factory=list)
    layers: list[str] = Field(default_factory=list)
    requires_plugins: list[str] = Field(default_factory=list)

    # Banner
    banner: Optional[BannerConfig] = None

    @field_validator("tags")
    @classmethod
    def validate_tags(cls, v: list[str]) -> list[str]:
        """Validate and normalize tags."""
        return [tag.lower().strip() for tag in v]

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: str) -> str:
        """Validate version format."""
        # Simple semver check
        parts = v.split(".")
        if len(parts) < 2:
            raise ValueError("Version must be in format: major.minor[.patch]")
        return v


class ThemeLoader:
    """Load and parse theme files."""

    def __init__(self):
        self._theme_cache: dict[str, ThemeConfig] = {}
        self._layer_cache: dict[str, LayerConfig] = {}

    def load_theme(self, theme_name: str) -> ThemeConfig:
        """
        Load a theme by name.

        Args:
            theme_name: Name of the theme (without .json extension)

        Returns:
            Parsed ThemeConfig

        Raises:
            FileNotFoundError: If theme file doesn't exist
            ValidationError: If theme JSON is invalid
        """
        # Check cache first
        if theme_name in self._theme_cache:
            return self._theme_cache[theme_name]

        # Search in builtin themes first
        theme_path = BUILTIN_THEMES_DIR / f"{theme_name}.json"

        # Then check community themes
        if not theme_path.exists():
            theme_path = COMMUNITY_THEMES_DIR / f"{theme_name}.json"

        if not theme_path.exists():
            raise FileNotFoundError(f"Theme '{theme_name}' not found")

        # Load and parse
        theme = self._load_from_file(theme_path, ThemeConfig)
        self._theme_cache[theme_name] = theme
        return theme

    def load_layer(self, layer_name: str) -> LayerConfig:
        """
        Load a layer by name.

        Args:
            layer_name: Name of the layer (without .json extension)

        Returns:
            Parsed LayerConfig

        Raises:
            FileNotFoundError: If layer file doesn't exist
        """
        # Check cache first
        if layer_name in self._layer_cache:
            return self._layer_cache[layer_name]

        layer_path = LAYERS_DIR / f"{layer_name}.json"

        if not layer_path.exists():
            raise FileNotFoundError(f"Layer '{layer_name}' not found")

        layer = self._load_from_file(layer_path, LayerConfig)
        self._layer_cache[layer_name] = layer
        return layer

    def _load_from_file(self, path: Path, model_class: type) -> Union[ThemeConfig, LayerConfig]:
        """Load and validate JSON file."""
        with open(path, "r") as f:
            data = json.load(f)

        return model_class(**data)

    def list_themes(self) -> list[str]:
        """List all available themes."""
        themes = set()

        # Builtin themes
        if BUILTIN_THEMES_DIR.exists():
            for f in BUILTIN_THEMES_DIR.glob("*.json"):
                themes.add(f.stem)

        # Community themes
        if COMMUNITY_THEMES_DIR.exists():
            for f in COMMUNITY_THEMES_DIR.glob("*.json"):
                themes.add(f.stem)

        return sorted(themes)

    def list_layers(self) -> list[str]:
        """List all available layers."""
        layers = set()

        if LAYERS_DIR.exists():
            for f in LAYERS_DIR.glob("*.json"):
                layers.add(f.stem)

        return sorted(layers)

    def get_theme_info(self, theme_name: str) -> dict:
        """Get theme metadata."""
        try:
            theme = self.load_theme(theme_name)
            return {
                "name": theme.name,
                "version": theme.version,
                "author": theme.author,
                "description": theme.description,
                "tags": theme.tags,
                "widgets": theme.widgets,
                "layers": theme.layers,
            }
        except FileNotFoundError:
            return {}

    def clear_cache(self) -> None:
        """Clear theme cache."""
        self._theme_cache.clear()
        self._layer_cache.clear()


# Singleton instance
_loader = ThemeLoader()


def load_theme(theme_name: str) -> ThemeConfig:
    """Load a theme by name."""
    return _loader.load_theme(theme_name)


def load_layer(layer_name: str) -> LayerConfig:
    """Load a layer by name."""
    return _loader.load_layer(layer_name)


def list_themes() -> list[str]:
    """List all available themes."""
    return _loader.list_themes()


def list_layers() -> list[str]:
    """List all available layers."""
    return _loader.list_layers()


__all__ = [
    "ThemeConfig",
    "LayerConfig",
    "ThemeLoader",
    "load_theme",
    "load_layer",
    "list_themes",
    "list_layers",
]
