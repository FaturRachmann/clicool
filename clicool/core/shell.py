"""Shell detection and abstraction layer."""

import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class ShellType(Enum):
    """Supported shell types."""

    BASH = "bash"
    ZSH = "zsh"
    FISH = "fish"
    UNKNOWN = "unknown"


@dataclass
class ShellInfo:
    """Information about detected shell."""

    shell_type: ShellType
    version: str
    config_path: Path
    is_login_shell: bool
    is_interactive: bool


class ShellDetector:
    """Detect and manage shell environments."""

    # Shell config file mappings
    SHELL_CONFIGS = {
        ShellType.BASH: ".bashrc",
        ShellType.ZSH: ".zshrc",
        ShellType.FISH: ".config/fish/config.fish",
    }

    # Shell executable names
    SHELL_EXECUTABLES = {
        "bash": ShellType.BASH,
        "zsh": ShellType.ZSH,
        "fish": ShellType.FISH,
    }

    def detect(self) -> ShellInfo:
        """
        Detect the current shell environment.

        Returns:
            ShellInfo with detected shell details
        """
        shell_type = self._detect_shell_type()
        version = self._get_shell_version(shell_type)
        config_path = self._find_shell_config(shell_type)
        is_login = self._is_login_shell()
        is_interactive = self._is_interactive_shell()

        return ShellInfo(
            shell_type=shell_type,
            version=version,
            config_path=config_path,
            is_login_shell=is_login,
            is_interactive=is_interactive,
        )

    def _detect_shell_type(self) -> ShellType:
        """Detect shell type from environment."""
        # Check SHELL environment variable
        shell_env = os.environ.get("SHELL", "")
        if shell_env:
            shell_name = Path(shell_env).name
            if shell_name in self.SHELL_EXECUTABLES:
                return self.SHELL_EXECUTABLES[shell_name]

        # Check current process
        try:
            result = subprocess.run(
                ["ps", "-p", str(os.getpid()), "-o", "comm="],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                shell_name = result.stdout.strip()
                if shell_name in self.SHELL_EXECUTABLES:
                    return self.SHELL_EXECUTABLES[shell_name]
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Check parent process
        try:
            result = subprocess.run(
                ["ps", "-p", str(os.getppid()), "-o", "comm="],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                shell_name = result.stdout.strip()
                if shell_name in self.SHELL_EXECUTABLES:
                    return self.SHELL_EXECUTABLES[shell_name]
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        # Fallback: check common shells
        for shell_name, shell_type in self.SHELL_EXECUTABLES.items():
            if self._shell_exists(shell_name):
                return shell_type

        return ShellType.UNKNOWN

    def _shell_exists(self, shell_name: str) -> bool:
        """Check if a shell executable exists."""
        try:
            result = subprocess.run(
                ["which", shell_name],
                capture_output=True,
                timeout=5,
            )
            return result.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError):
            return False

    def _get_shell_version(self, shell_type: ShellType) -> str:
        """Get shell version string."""
        if shell_type == ShellType.UNKNOWN:
            return "unknown"

        try:
            result = subprocess.run(
                [shell_type.value, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                # Parse first line of version output
                first_line = result.stdout.split("\n")[0]
                return first_line.strip()
        except (subprocess.SubprocessError, FileNotFoundError, TimeoutError):
            pass

        return "unknown"

    def _find_shell_config(self, shell_type: ShellType) -> Path:
        """Find the shell configuration file."""
        if shell_type == ShellType.UNKNOWN:
            return Path.home() / ".bashrc"  # Default fallback

        config_name = self.SHELL_CONFIGS.get(shell_type, ".bashrc")
        config_path = Path.home() / config_name

        # If config doesn't exist, try to create it
        if not config_path.exists():
            # For fish, check alternative locations
            if shell_type == ShellType.FISH:
                alt_config = Path.home() / ".config" / "fish" / "config.fish"
                if alt_config.exists():
                    return alt_config

        return config_path

    def _is_login_shell(self) -> bool:
        """Check if current shell is a login shell."""
        # Check if SHELL is set and we're in a login context
        return (
            os.environ.get("LOGIN_SHELL", "0") == "1" or os.environ.get("BASH_VERSION") is not None
        )

    def _is_interactive_shell(self) -> bool:
        """Check if current shell is interactive."""
        # Check if we have a terminal
        return os.isatty(0)

    def get_config_path(self, shell_type: ShellType | None = None) -> Path:
        """
        Get the config path for a shell type.

        Args:
            shell_type: Shell type, or None to auto-detect

        Returns:
            Path to shell config file
        """
        if shell_type is None:
            shell_type = self.detect().shell_type

        if shell_type == ShellType.UNKNOWN:
            return Path.home() / ".bashrc"

        config_name = self.SHELL_CONFIGS.get(shell_type, ".bashrc")
        return Path.home() / config_name

    def list_available_shells(self) -> list[ShellType]:
        """List all available shells on the system."""
        available = []
        for shell_name, shell_type in self.SHELL_EXECUTABLES.items():
            if self._shell_exists(shell_name):
                available.append(shell_type)
        return available


# Singleton instance
_detector = ShellDetector()


def detect_shell() -> ShellInfo:
    """Detect current shell environment."""
    return _detector.detect()


def get_shell_config_path(shell_type: ShellType | None = None) -> Path:
    """Get shell config path."""
    return _detector.get_config_path(shell_type)


__all__ = [
    "ShellType",
    "ShellInfo",
    "ShellDetector",
    "detect_shell",
    "get_shell_config_path",
]
