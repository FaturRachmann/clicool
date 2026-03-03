"""Tests for config injector."""

import pytest
from pathlib import Path

from clicool.core.injector import ConfigInjector, START_MARKER, END_MARKER


class TestConfigInjector:
    """Test config injection functionality."""

    def test_injector_initialization(self):
        """Test ConfigInjector initialization."""
        injector = ConfigInjector()
        assert injector is not None
        assert injector.dry_run is False

    def test_injector_dry_run(self):
        """Test ConfigInjector with dry run mode."""
        injector = ConfigInjector(dry_run=True)
        assert injector.dry_run is True

    def test_is_injected_file_not_exists(self, temp_dir):
        """Test is_injected when file doesn't exist."""
        injector = ConfigInjector()
        config_path = temp_dir / "nonexistent"
        
        result = injector.is_injected(config_path, "test_theme")
        assert result is False

    def test_is_injected_false(self, sample_shell_config):
        """Test is_injected when theme is not injected."""
        injector = ConfigInjector()
        
        result = injector.is_injected(sample_shell_config, "nonexistent_theme")
        assert result is False

    def test_is_injected_true(self, sample_config_with_markers):
        """Test is_injected when theme is injected."""
        injector = ConfigInjector()
        
        result = injector.is_injected(sample_config_with_markers, "test_theme")
        assert result is True

    def test_get_injected_themes_empty(self, sample_shell_config):
        """Test get_injected_themes when no themes injected."""
        injector = ConfigInjector()
        
        themes = injector.get_injected_themes(sample_shell_config)
        assert themes == []

    def test_get_injected_themes(self, sample_config_with_markers):
        """Test get_injected_themes with injected themes."""
        injector = ConfigInjector()
        
        themes = injector.get_injected_themes(sample_config_with_markers)
        assert "test_theme" in themes

    def test_extract_block_not_found(self, sample_shell_config):
        """Test extract_block when block not found."""
        injector = ConfigInjector()
        
        block = injector.extract_block(sample_shell_config, "nonexistent")
        assert block is None

    def test_extract_block(self, sample_config_with_markers):
        """Test extracting injected block."""
        injector = ConfigInjector()
        
        block = injector.extract_block(sample_config_with_markers, "test_theme")
        assert block is not None
        assert "PS1=" in block

    def test_remove_not_exists(self, temp_dir):
        """Test remove when file doesn't exist."""
        injector = ConfigInjector()
        config_path = temp_dir / "nonexistent"
        
        success, message = injector.remove(config_path, "test_theme")
        assert success is False

    def test_remove_not_injected(self, sample_shell_config):
        """Test remove when theme not injected."""
        injector = ConfigInjector()
        
        success, message = injector.remove(sample_shell_config, "nonexistent")
        assert success is False

    def test_inject_new_file(self, temp_dir):
        """Test injecting into new file."""
        injector = ConfigInjector()
        config_path = temp_dir / "new_config"
        
        content = "PS1='\\u@\\h:\\w$ '"
        success, message = injector.inject(config_path, content, "new_theme")
        
        assert success is True
        assert config_path.exists()
        
        # Verify content
        with open(config_path, "r") as f:
            file_content = f.read()
        assert START_MARKER.format(theme="new_theme") in file_content
        assert content in file_content

    def test_inject_existing_file(self, sample_shell_config):
        """Test injecting into existing file."""
        injector = ConfigInjector()
        
        content = "PS1='custom'"
        success, message = injector.inject(sample_shell_config, content, "new_theme")
        
        assert success is True
        
        # Verify content added
        with open(sample_shell_config, "r") as f:
            file_content = f.read()
        assert START_MARKER.format(theme="new_theme") in file_content

    def test_inject_update_existing(self, sample_config_with_markers):
        """Test updating existing injection."""
        injector = ConfigInjector()
        
        new_content = "PS1='updated'"
        success, message = injector.inject(
            sample_config_with_markers, 
            new_content, 
            "test_theme"
        )
        
        assert success is True
        
        # Verify content updated
        with open(sample_config_with_markers, "r") as f:
            file_content = f.read()
        assert new_content in file_content

    def test_dry_run_inject(self, temp_dir):
        """Test dry run injection."""
        injector = ConfigInjector(dry_run=True)
        config_path = temp_dir / "config"
        config_path.touch()
        
        content = "PS1='test'"
        success, message = injector.inject(config_path, content, "dry_theme")
        
        assert success is True
        # File should not be modified in dry run
        with open(config_path, "r") as f:
            assert f.read() == ""

    def test_dry_run_remove(self, sample_config_with_markers):
        """Test dry run remove."""
        injector = ConfigInjector(dry_run=True)
        
        success, message = injector.remove(sample_config_with_markers, "test_theme")
        
        assert success is True
        # File should not be modified in dry run
        with open(sample_config_with_markers, "r") as f:
            content = f.read()
        assert START_MARKER.format(theme="test_theme") in content
