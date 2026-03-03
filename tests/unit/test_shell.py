"""Tests for shell detection."""

import os
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock

from clicool.core.shell import ShellDetector, ShellType, ShellInfo


class TestShellDetector:
    """Test shell detection functionality."""

    def test_shell_type_enum(self):
        """Test ShellType enum values."""
        assert ShellType.BASH.value == "bash"
        assert ShellType.ZSH.value == "zsh"
        assert ShellType.FISH.value == "fish"
        assert ShellType.UNKNOWN.value == "unknown"

    def test_shell_detector_initialization(self):
        """Test ShellDetector initialization."""
        detector = ShellDetector()
        assert detector is not None
        assert hasattr(detector, 'SHELL_CONFIGS')
        assert hasattr(detector, 'SHELL_EXECUTABLES')

    def test_shell_config_mappings(self):
        """Test shell config file mappings."""
        detector = ShellDetector()
        
        assert detector.SHELL_CONFIGS[ShellType.BASH] == ".bashrc"
        assert detector.SHELL_CONFIGS[ShellType.ZSH] == ".zshrc"
        assert detector.SHELL_CONFIGS[ShellType.FISH] == ".config/fish/config.fish"

    def test_get_config_path_bash(self):
        """Test getting bash config path."""
        detector = ShellDetector()
        config_path = detector.get_config_path(ShellType.BASH)
        
        assert config_path == Path.home() / ".bashrc"

    def test_get_config_path_zsh(self):
        """Test getting zsh config path."""
        detector = ShellDetector()
        config_path = detector.get_config_path(ShellType.ZSH)
        
        assert config_path == Path.home() / ".zshrc"

    def test_get_config_path_unknown(self):
        """Test getting config path for unknown shell."""
        detector = ShellDetector()
        config_path = detector.get_config_path(ShellType.UNKNOWN)
        
        # Should default to .bashrc
        assert config_path == Path.home() / ".bashrc"

    @patch('subprocess.run')
    def test_shell_exists_true(self, mock_run):
        """Test shell exists check when shell is found."""
        mock_run.return_value = MagicMock(returncode=0)
        
        detector = ShellDetector()
        result = detector._shell_exists("bash")
        
        assert result is True
        mock_run.assert_called_once()

    @patch('subprocess.run')
    def test_shell_exists_false(self, mock_run):
        """Test shell exists check when shell is not found."""
        mock_run.return_value = MagicMock(returncode=1)
        
        detector = ShellDetector()
        result = detector._shell_exists("nonexistent_shell")
        
        assert result is False

    @patch('subprocess.run')
    def test_get_shell_version(self, mock_run):
        """Test getting shell version."""
        mock_run.return_value = MagicMock(
            returncode=0,
            stdout="bash, version 5.2.15(1)-release\n"
        )
        
        detector = ShellDetector()
        version = detector._get_shell_version(ShellType.BASH)
        
        assert version != ""
        assert "bash" in version.lower() or "5.2" in version

    @patch('os.environ.get')
    def test_detect_from_shell_env(self, mock_environ_get):
        """Test shell detection from SHELL environment variable."""
        mock_environ_get.side_effect = lambda key, default=None: (
            "/bin/zsh" if key == "SHELL" else default
        )
        
        detector = ShellDetector()
        shell_type = detector._detect_shell_type()
        
        assert shell_type == ShellType.ZSH

    def test_list_available_shells(self):
        """Test listing available shells."""
        detector = ShellDetector()
        shells = detector.list_available_shells()
        
        # Should return a list
        assert isinstance(shells, list)
        
        # At least one shell should be available
        # (might be empty in test environment)
        for shell in shells:
            assert shell in [ShellType.BASH, ShellType.ZSH, ShellType.FISH]


class TestShellInfo:
    """Test ShellInfo dataclass."""

    def test_shell_info_creation(self):
        """Test creating ShellInfo instance."""
        info = ShellInfo(
            shell_type=ShellType.BASH,
            version="bash 5.2.15",
            config_path=Path.home() / ".bashrc",
            is_login_shell=True,
            is_interactive=True,
        )
        
        assert info.shell_type == ShellType.BASH
        assert info.version == "bash 5.2.15"
        assert info.is_login_shell is True
        assert info.is_interactive is True
