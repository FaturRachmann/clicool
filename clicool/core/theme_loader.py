"""Theme loader and parser for clicool theme JSON files."""

import json
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from .. import BUILTIN_THEMES_DIR, COMMUNITY_THEMES_DIR, LAYERS_DIR


class ColorConfig(BaseModel):
    """Color configuration for theme elements."""

    user: str | None = None
    host: str | None = None
    path: str | None = None
    git_branch: str | None = None
    symbol: str | None = None
    # Additional colors
    background: str | None = None
    foreground: str | None = None
    cursor: str | None = None
    selection: str | None = None


class IconConfig(BaseModel):
    """Icon configuration for theme elements."""

    user: str | None = None
    git: str | None = None
    error: str | None = None
    # Additional icons
    success: str | None = None
    warning: str | None = None
    info: str | None = None


class PromptConfig(BaseModel):
    """Prompt configuration."""

    format: str = "default"
    template: str | None = None
    colors: ColorConfig | None = None
    icons: IconConfig | None = None


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

    background: str | None = None
    foreground: str | None = None
    cursor: str | None = None
    selection: str | None = None
    ansi: list[str] | None = None


class TerminalConfig(BaseModel):
    """Terminal configuration."""

    color_palette: TerminalColorPalette | None = None
    font_recommendation: str | None = None
    opacity: float | None = Field(default=None, ge=0.0, le=1.0)


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
    widget: WidgetConfig | None = None


class ThemeConfig(BaseModel):
    """Main theme configuration model."""

    schema_url: str | None = Field(default=None, alias="$schema")
    name: str
    version: str = "1.0.0"
    author: str | None = None
    description: str | None = None
    tags: list[str] = Field(default_factory=list)
    type: str = "theme"  # "theme" or "layer"

    # Prompt configuration
    prompt: PromptConfig | None = None

    # Features
    features: FeaturesConfig | None = None

    # Terminal configuration
    terminal: TerminalConfig | None = None

    # Widgets and layers
    widgets: list[str] = Field(default_factory=list)
    layers: list[str] = Field(default_factory=list)
    requires_plugins: list[str] = Field(default_factory=list)

    # Banner
    banner: BannerConfig | None = None

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
        self._layer_cache[layer_name] = layer  # type: ignore
        return layer  # type: ignore

    def _load_from_file(self, path: Path, model_class: type) -> ThemeConfig | LayerConfig:
        """Load and validate JSON file."""
        with open(path) as f:
            data = json.load(f)

        return model_class(**data)  # type: ignore

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
