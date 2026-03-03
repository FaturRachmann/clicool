"""Tests for theme loader."""

import json
import pytest
from pathlib import Path

from clicool.core.theme_loader import ThemeLoader, ThemeConfig, LayerConfig
from clicool.core.validator import ThemeValidator, validate_file


class TestThemeLoader:
    """Test theme loading functionality."""

    def test_load_theme_from_file(self, sample_theme_file, sample_theme_json):
        """Test loading theme from JSON file."""
        loader = ThemeLoader()
        theme = loader._load_from_file(sample_theme_file, ThemeConfig)
        
        assert theme.name == sample_theme_json["name"]
        assert theme.version == sample_theme_json["version"]
        assert theme.description == sample_theme_json["description"]
        assert theme.tags == sample_theme_json["tags"]

    def test_theme_config_validation(self, sample_theme_json):
        """Test theme config validation with Pydantic."""
        theme = ThemeConfig(**sample_theme_json)
        
        assert theme.name == "Test Theme"
        assert theme.version == "1.0.0"
        assert theme.prompt is not None
        assert theme.prompt.format == "neon"
        assert theme.features is not None
        assert theme.features.show_git is True

    def test_theme_config_missing_required_fields(self):
        """Test validation fails for missing required fields."""
        invalid_theme = {
            "version": "1.0.0",
            # Missing "name"
        }
        
        with pytest.raises(Exception):
            ThemeConfig(**invalid_theme)

    def test_theme_config_invalid_version(self):
        """Test validation fails for invalid version format."""
        invalid_theme = {
            "name": "Test",
            "version": "invalid",  # Should be like "1.0" or "1.0.0"
        }
        
        with pytest.raises(Exception):
            ThemeConfig(**invalid_theme)


class TestLayerLoader:
    """Test layer loading functionality."""

    def test_load_layer_from_dict(self, sample_layer_json):
        """Test loading layer from dictionary."""
        layer = LayerConfig(**sample_layer_json)
        
        assert layer.name == "Test Layer"
        assert layer.type == "layer"
        assert layer.version == "1.0.0"
        assert layer.widget is not None
        assert layer.widget.name == "test-widget"

    def test_layer_config_defaults(self):
        """Test layer config default values."""
        layer = LayerConfig(name="Simple Layer")
        
        assert layer.type == "layer"
        assert layer.version == "1.0.0"
        assert layer.widget is None


class TestThemeValidator:
    """Test theme validation."""

    def test_validate_valid_theme(self, sample_theme_json):
        """Test validating a valid theme."""
        validator = ThemeValidator()
        result = validator.validate_theme(sample_theme_json)
        
        assert result.valid is True
        assert len(result.errors) == 0

    def test_validate_invalid_theme(self):
        """Test validating an invalid theme."""
        validator = ThemeValidator()
        result = validator.validate_theme({})
        
        assert result.valid is False
        assert len(result.errors) > 0

    def test_validate_prompt_format(self, sample_theme_json):
        """Test prompt format validation."""
        sample_theme_json["prompt"]["format"] = "invalid_format"
        
        validator = ThemeValidator()
        result = validator.validate_theme(sample_theme_json)
        
        # Should have error about invalid format
        assert any("prompt format" in str(e).lower() for e in result.errors)

    def test_validate_animation(self, sample_theme_json):
        """Test animation validation."""
        sample_theme_json["banner"]["animation"] = "invalid_animation"
        
        validator = ThemeValidator()
        result = validator.validate_theme(sample_theme_json)
        
        # Should have error about invalid animation
        assert any("animation" in str(e).lower() for e in result.errors)

    def test_validate_opacity_range(self, sample_theme_json):
        """Test opacity range validation."""
        sample_theme_json["terminal"]["opacity"] = 1.5  # Out of range
        
        validator = ThemeValidator()
        result = validator.validate_theme(sample_theme_json)
        
        assert result.valid is False
        assert any("opacity" in str(e).lower() for e in result.errors)

    def test_validate_file(self, sample_theme_file):
        """Test file validation."""
        result = validate_file(sample_theme_file)
        assert result.valid is True

    def test_validate_nonexistent_file(self):
        """Test validation of nonexistent file."""
        result = validate_file(Path("/nonexistent/path.json"))
        assert result.valid is False
        assert any("not found" in str(e).lower() for e in result.errors)

    def test_validate_invalid_json(self, temp_dir):
        """Test validation of invalid JSON file."""
        invalid_json = temp_dir / "invalid.json"
        invalid_json.write_text("{ invalid json }")
        
        result = validate_file(invalid_json)
        assert result.valid is False
