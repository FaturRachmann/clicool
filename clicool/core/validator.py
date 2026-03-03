"""JSON Schema validator for clicool themes."""

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .theme_loader import LayerConfig, ThemeConfig


class ValidationResult:
    """Result of theme validation."""

    def __init__(self, valid: bool, errors: list[str] | None = None):
        self.valid = valid
        self.errors = errors or []

    def __bool__(self) -> bool:
        return self.valid

    def __str__(self) -> str:
        if self.valid:
            return "Validation passed ✓"
        return "Validation failed ✗\n" + "\n".join(f"  - {e}" for e in self.errors)


class ThemeValidator:
    """Validate theme JSON files against schema."""

    # Required fields for themes
    THEME_REQUIRED_FIELDS = ["name", "version"]

    # Required fields for layers
    LAYER_REQUIRED_FIELDS = ["name", "type", "version"]

    # Valid prompt formats
    VALID_PROMPT_FORMATS = [
        "default",
        "neon",
        "powerline",
        "minimal",
        "classic",
        "rainbow",
    ]

    # Valid animation styles
    VALID_ANIMATIONS = [
        "none",
        "typewriter",
        "fade-in",
        "slide-in",
        "glitch",
        "matrix",
        "neon-pulse",
    ]

    def validate_theme(self, theme_data: dict[str, Any]) -> ValidationResult:
        """
        Validate theme data.

        Args:
            theme_data: Parsed theme JSON data

        Returns:
            ValidationResult with success status and errors
        """
        errors = []

        # Check required fields
        for field in self.THEME_REQUIRED_FIELDS:
            if field not in theme_data:
                errors.append(f"Missing required field: {field}")

        # Validate version format
        if "version" in theme_data:
            version = theme_data["version"]
            if not self._is_valid_version(version):
                errors.append(f"Invalid version format: {version}")

        # Validate prompt format if present
        if "prompt" in theme_data and theme_data["prompt"]:
            prompt_format = theme_data["prompt"].get("format", "default")
            if prompt_format not in self.VALID_PROMPT_FORMATS:
                errors.append(
                    f"Invalid prompt format: {prompt_format}. "
                    f"Valid formats: {', '.join(self.VALID_PROMPT_FORMATS)}"
                )

        # Validate banner animation if present
        if "banner" in theme_data and theme_data["banner"]:
            animation = theme_data["banner"].get("animation", "none")
            if animation not in self.VALID_ANIMATIONS:
                errors.append(
                    f"Invalid animation: {animation}. "
                    f"Valid animations: {', '.join(self.VALID_ANIMATIONS)}"
                )

        # Validate opacity if present
        if "terminal" in theme_data and theme_data["terminal"]:
            opacity = theme_data["terminal"].get("opacity")
            if opacity is not None:
                if not (0.0 <= opacity <= 1.0):
                    errors.append(f"Opacity must be between 0.0 and 1.0, got: {opacity}")

        # Try to parse with Pydantic for full validation
        if not errors:
            try:
                ThemeConfig(**theme_data)
            except ValidationError as e:
                for error in e.errors():
                    field = ".".join(str(x) for x in error["loc"])
                    errors.append(f"{field}: {error['msg']}")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def validate_layer(self, layer_data: dict[str, Any]) -> ValidationResult:
        """
        Validate layer data.

        Args:
            layer_data: Parsed layer JSON data

        Returns:
            ValidationResult with success status and errors
        """
        errors = []

        # Check required fields
        for field in self.LAYER_REQUIRED_FIELDS:
            if field not in layer_data:
                errors.append(f"Missing required field: {field}")

        # Check type is 'layer'
        if "type" in layer_data and layer_data["type"] != "layer":
            errors.append(f"Layer type must be 'layer', got: {layer_data['type']}")

        # Validate version format
        if "version" in layer_data:
            version = layer_data["version"]
            if not self._is_valid_version(version):
                errors.append(f"Invalid version format: {version}")

        # Try to parse with Pydantic for full validation
        if not errors:
            try:
                LayerConfig(**layer_data)
            except ValidationError as e:
                for error in e.errors():
                    field = ".".join(str(x) for x in error["loc"])
                    errors.append(f"{field}: {error['msg']}")

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def validate_file(self, file_path: Path) -> ValidationResult:
        """
        Validate a theme or layer file.

        Args:
            file_path: Path to JSON file

        Returns:
            ValidationResult with success status and errors
        """
        if not file_path.exists():
            return ValidationResult(valid=False, errors=[f"File not found: {file_path}"])

        try:
            with open(file_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return ValidationResult(valid=False, errors=[f"Invalid JSON: {e}"])

        # Determine if it's a theme or layer based on 'type' field
        data_type = data.get("type", "theme")

        if data_type == "layer":
            return self.validate_layer(data)
        else:
            return self.validate_theme(data)

    def _is_valid_version(self, version: str) -> bool:
        """Check if version string is valid semver-like."""
        parts = version.split(".")
        if len(parts) < 2:
            return False

        try:
            # First two parts must be integers
            int(parts[0])
            int(parts[1])
            return True
        except ValueError:
            return False


# Singleton instance
_validator = ThemeValidator()


def validate_theme(theme_data: dict) -> ValidationResult:
    """Validate theme data."""
    return _validator.validate_theme(theme_data)


def validate_layer(layer_data: dict) -> ValidationResult:
    """Validate layer data."""
    return _validator.validate_layer(layer_data)


def validate_file(file_path: Path) -> ValidationResult:
    """Validate a theme or layer file."""
    return _validator.validate_file(file_path)


__all__ = [
    "ValidationResult",
    "ThemeValidator",
    "validate_theme",
    "validate_layer",
    "validate_file",
]
