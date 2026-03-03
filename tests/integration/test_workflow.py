"""Integration tests for clicool."""

import pytest
from pathlib import Path

from clicool.core.theme_loader import ThemeLoader, list_themes
from clicool.core.injector import ConfigInjector
from clicool.core.generator import PromptGenerator, FunctionGenerator
from clicool.core.validator import validate_file
from clicool.safety.backup import BackupManager


class TestBuiltinThemes:
    """Test builtin themes are valid and loadable."""

    def test_list_builtin_themes(self, builtin_themes_dir):
        """Test listing builtin themes."""
        themes = list_themes()
        
        # Should have at least our 5 themes
        assert len(themes) >= 5
        
        expected_themes = ["cyberpunk", "matrix", "retro", "minimal", "devops"]
        for theme_name in expected_themes:
            assert theme_name in themes

    def test_load_cyberpunk_theme(self):
        """Test loading cyberpunk theme."""
        loader = ThemeLoader()
        theme = loader.load_theme("cyberpunk")
        
        assert theme.name == "Cyberpunk"
        assert theme.version == "1.0.0"
        assert theme.prompt is not None
        assert theme.terminal is not None

    def test_load_matrix_theme(self):
        """Test loading matrix theme."""
        loader = ThemeLoader()
        theme = loader.load_theme("matrix")
        
        assert theme.name == "Matrix"
        assert theme.tags is not None
        assert "matrix" in theme.tags or "hacker" in theme.tags

    def test_load_devops_theme(self):
        """Test loading devops theme."""
        loader = ThemeLoader()
        theme = loader.load_theme("devops")
        
        assert theme.name == "DevOps Pro"
        assert theme.widgets is not None
        assert len(theme.widgets) > 0

    def test_all_builtin_themes_valid(self, builtin_themes_dir):
        """Test all builtin themes are valid JSON."""
        loader = ThemeLoader()
        
        for theme_name in list_themes():
            theme = loader.load_theme(theme_name)
            assert theme is not None
            assert theme.name is not None
            assert theme.version is not None


class TestLayers:
    """Test layer themes."""

    def test_list_layers(self, layers_dir):
        """Test listing available layers."""
        loader = ThemeLoader()
        layers = loader.list_layers()
        
        # Should have at least our 4 layers
        assert len(layers) >= 4
        
        expected_layers = ["git-status", "k8s-context", "docker-info", "aws-profile"]
        for layer_name in expected_layers:
            assert layer_name in layers

    def test_load_git_status_layer(self):
        """Test loading git-status layer."""
        loader = ThemeLoader()
        layer = loader.load_layer("git-status")
        
        assert layer.name == "Git Status"
        assert layer.type == "layer"
        assert layer.widget is not None
        assert layer.widget.name == "git-status"


class TestThemeGeneration:
    """Test theme generation for different shells."""

    def test_generate_bash_prompt(self):
        """Test generating bash prompt."""
        loader = ThemeLoader()
        theme = loader.load_theme("cyberpunk")
        
        generator = PromptGenerator()
        config = generator.generate(theme, "bash")
        
        assert config is not None
        assert "PS1=" in config or "clicool_" in config

    def test_generate_zsh_prompt(self):
        """Test generating zsh prompt."""
        loader = ThemeLoader()
        theme = loader.load_theme("cyberpunk")
        
        generator = PromptGenerator()
        config = generator.generate(theme, "zsh")
        
        assert config is not None

    def test_generate_functions(self):
        """Test generating helper functions."""
        func_gen = FunctionGenerator()
        functions = func_gen.generate_all()
        
        assert functions is not None
        assert "clicool_git_branch" in functions
        assert "clicool_exit_code" in functions


class TestBackupRestore:
    """Test backup and restore functionality."""

    def test_create_backup(self, sample_shell_config):
        """Test creating a backup."""
        backup_manager = BackupManager()
        
        backup = backup_manager.create_backup(
            sample_shell_config,
            "bash",
            "test_theme"
        )
        
        assert backup is not None
        assert backup.backup_id is not None
        assert backup.shell == "bash"
        assert backup.theme == "test_theme"

    def test_list_backups(self, sample_shell_config):
        """Test listing backups."""
        backup_manager = BackupManager()
        
        # Create a backup first
        backup_manager.create_backup(sample_shell_config, "bash", "test")
        
        backups = backup_manager.list_backups()
        assert len(backups) > 0

    def test_backup_content_matches_original(self, sample_shell_config):
        """Test backup content matches original."""
        backup_manager = BackupManager()
        
        # Read original
        original_content = sample_shell_config.read_text()
        
        # Create backup
        backup = backup_manager.create_backup(sample_shell_config, "bash", "test")
        
        # Get backup content
        backup_content = backup_manager.get_backup_content(backup.backup_id)
        
        assert backup_content == original_content


class TestInjectionWorkflow:
    """Test complete injection workflow."""

    def test_full_injection_cycle(self, temp_dir):
        """Test complete injection and removal cycle."""
        # Setup
        config_path = temp_dir / ".bashrc"
        config_path.write_text("# Original config\n")
        
        loader = ThemeLoader()
        theme = loader.load_theme("minimal")
        
        generator = PromptGenerator()
        config_content = generator.generate(theme, "bash")
        
        injector = ConfigInjector()
        
        # Inject
        success, message = injector.inject(config_path, config_content, "minimal")
        assert success is True
        assert injector.is_injected(config_path, "minimal") is True
        
        # Remove
        success, message = injector.remove(config_path, "minimal")
        assert success is True
        assert injector.is_injected(config_path, "minimal") is False

    def test_injection_preserves_existing_config(self, sample_shell_config):
        """Test that injection preserves existing config."""
        original_content = sample_shell_config.read_text()
        
        loader = ThemeLoader()
        theme = loader.load_theme("minimal")
        
        generator = PromptGenerator()
        config_content = generator.generate(theme, "bash")
        
        injector = ConfigInjector()
        injector.inject(sample_shell_config, config_content, "test")
        
        # Read new content
        new_content = sample_shell_config.read_text()
        
        # Original content should still be there
        assert "# Sample bashrc" in new_content
        assert "alias ll='ls -la'" in new_content
