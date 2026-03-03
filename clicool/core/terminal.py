"""Terminal emulator detection and capability probing."""

import os
import subprocess
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class TerminalType(Enum):
    """Known terminal emulators."""

    GNOME_TERMINAL = "gnome-terminal"
    KITTY = "kitty"
    ALACRITTY = "alacritty"
    ITERM2 = "iterm2"
    WINDOWS_TERMINAL = "windows-terminal"
    KONSOLE = "konsole"
    WEZTERM = "wezterm"
    HYPER = "hyper"
    TERMINATOR = "terminator"
    XFCE4_TERMINAL = "xfce4-terminal"
    ST = "st"
    URXVT = "urxvt"
    UNKNOWN = "unknown"


@dataclass
class TerminalInfo:
    """Information about detected terminal."""

    terminal_type: TerminalType
    name: str
    version: Optional[str]
    supports_true_color: bool
    supports_256_color: bool
    supports_unicode: bool
    supports_hyperlinks: bool
    font_name: Optional[str]
    font_size: Optional[int]
    columns: int
    rows: int


class TerminalProbe:
    """Probe terminal capabilities."""

    # Environment variable mappings for terminal detection
    ENV_MAPPINGS = {
        "KONSOLE_VERSION": TerminalType.KONSOLE,
        "KONSOLE_PROFILE_NAME": TerminalType.KONSOLE,
        "VTE_VERSION": TerminalType.GNOME_TERMINAL,
        "KITTY_PID": TerminalType.KITTY,
        "ALACRITTY_SOCKET": TerminalType.ALACRITTY,
        "WEZTERM_EXECUTABLE": TerminalType.WEZTERM,
        "ITERM_SESSION_ID": TerminalType.ITERM2,
        "WT_SESSION": TerminalType.WINDOWS_TERMINAL,
        "HYPER_TERM": TerminalType.HYPER,
        "TERMINATOR_UUID": TerminalType.TERMINATOR,
    }

    def detect(self) -> TerminalInfo:
        """Detect terminal emulator and capabilities."""
        terminal_type = self._detect_terminal_type()
        name = terminal_type.value
        version = self._get_terminal_version(terminal_type)
        true_color = self._check_true_color()
        color_256 = self._check_256_color()
        unicode_support = self._check_unicode_support()
        hyperlinks = self._check_hyperlinks()
        font_name, font_size = self._get_font_info()
        columns, rows = self._get_terminal_size()

        return TerminalInfo(
            terminal_type=terminal_type,
            name=name,
            version=version,
            supports_true_color=true_color,
            supports_256_color=color_256,
            supports_unicode=unicode_support,
            supports_hyperlinks=hyperlinks,
            font_name=font_name,
            font_size=font_size,
            columns=columns,
            rows=rows,
        )

    def _detect_terminal_type(self) -> TerminalType:
        """Detect terminal emulator type."""
        # Check environment variables
        for env_var, terminal_type in self.ENV_MAPPINGS.items():
            if os.environ.get(env_var):
                return terminal_type

        # Check TERM environment variable
        term = os.environ.get("TERM", "")
        if "kitty" in term:
            return TerminalType.KITTY
        elif "alacritty" in term:
            return TerminalType.ALACRITTY
        elif "xterm" in term or "gnome" in term:
            return TerminalType.GNOME_TERMINAL
        elif "konsole" in term:
            return TerminalType.KONSOLE
        elif "wezterm" in term:
            return TerminalType.WEZTERM
        elif "hyper" in term:
            return TerminalType.HYPER

        # Check running processes
        try:
            # Get parent process name
            result = subprocess.run(
                ["ps", "-p", str(os.getppid()), "-o", "comm="],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if result.returncode == 0:
                proc_name = result.stdout.strip().lower()
                for term_type in TerminalType:
                    if term_type.value in proc_name:
                        return term_type
        except (subprocess.SubprocessError, FileNotFoundError):
            pass

        return TerminalType.UNKNOWN

    def _get_terminal_version(self, terminal_type: TerminalType) -> Optional[str]:
        """Get terminal emulator version."""
        if terminal_type == TerminalType.UNKNOWN:
            return None

        try:
            # Try common version flags
            for flag in ["--version", "-v", "-V"]:
                try:
                    result = subprocess.run(
                        [terminal_type.value, flag],
                        capture_output=True,
                        text=True,
                        timeout=5,
                    )
                    if result.returncode == 0 and result.stdout.strip():
                        return result.stdout.strip().split("\n")[0]
                except (subprocess.SubprocessError, FileNotFoundError):
                    continue
        except (subprocess.SubprocessError, TimeoutError):
            pass

        # Check environment variables for version
        if terminal_type == TerminalType.KONSOLE:
            version = os.environ.get("KONSOLE_VERSION")
            if version:
                return version
        elif terminal_type == TerminalType.GNOME_TERMINAL:
            version = os.environ.get("VTE_VERSION")
            if version:
                return version

        return None

    def _check_true_color(self) -> bool:
        """Check if terminal supports true color (24-bit)."""
        # Check COLORTERM environment variable
        colorterm = os.environ.get("COLORTERM", "")
        if "truecolor" in colorterm or "24bit" in colorterm:
            return True

        # Check TERM for true color support
        term = os.environ.get("TERM", "")
        if "truecolor" in term or "24bit" in term:
            return True

        # Known true-color terminals
        true_color_terms = [
            "kitty",
            "alacritty",
            "wezterm",
            "iterm2",
            "gnome-terminal",
            "konsole",
            "hyper",
        ]
        for term_name in true_color_terms:
            if term_name in term.lower():
                return True

        # Try to query terminal using xterm sequence
        # This is a more reliable method but may not work in all terminals
        return self._query_true_color()

    def _query_true_color(self) -> bool:
        """Query terminal for true color support using escape sequences."""
        # This is a simplified check - full implementation would use
        # DA1/DA2 escape sequences
        term = os.environ.get("TERM", "")
        return "256" in term or "truecolor" in term.lower()

    def _check_256_color(self) -> bool:
        """Check if terminal supports 256 colors."""
        term = os.environ.get("TERM", "")
        if "256" in term:
            return True

        # Most modern terminals support 256 colors
        return self._check_true_color()

    def _check_unicode_support(self) -> bool:
        """Check if terminal supports Unicode."""
        # Check LANG environment variable
        lang = os.environ.get("LANG", "")
        if "UTF-8" in lang or "utf8" in lang:
            return True

        # Most modern terminals support Unicode
        return True

    def _check_hyperlinks(self) -> bool:
        """Check if terminal supports OSC 8 hyperlinks."""
        # Known terminals with hyperlink support
        hyperlink_terminals = [
            TerminalType.KITTY,
            TerminalType.WEZTERM,
            TerminalType.ITERM2,
            TerminalType.GNOME_TERMINAL,
            TerminalType.HYPER,
        ]

        terminal_type = self._detect_terminal_type()
        return terminal_type in hyperlink_terminals

    def _get_font_info(self) -> tuple[Optional[str], Optional[int]]:
        """Get terminal font information."""
        # This is difficult to query programmatically
        # Return None as default - user can configure manually
        return None, None

    def _get_terminal_size(self) -> tuple[int, int]:
        """Get terminal dimensions."""
        try:
            size = os.get_terminal_size()
            return size.columns, size.rows
        except OSError:
            return 80, 24  # Default fallback


# Singleton instance
_probe = TerminalProbe()


def detect_terminal() -> TerminalInfo:
    """Detect current terminal."""
    return _probe.detect()


__all__ = [
    "TerminalType",
    "TerminalInfo",
    "TerminalProbe",
    "detect_terminal",
]
