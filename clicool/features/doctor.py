"""Environment diagnostics - Doctor command implementation."""

import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ..core.shell import ShellDetector, ShellType
from ..core.terminal import TerminalProbe

console = Console()


class CheckStatus(Enum):
    """Status of a diagnostic check."""

    OK = "ok"
    WARNING = "warning"
    ERROR = "error"
    SKIPPED = "skipped"


@dataclass
class CheckResult:
    """Result of a single diagnostic check."""

    name: str
    status: CheckStatus
    message: str
    details: Optional[str] = None
    recommendation: Optional[str] = None


class Doctor:
    """Environment diagnostics tool."""

    def __init__(self):
        self.shell_detector = ShellDetector()
        self.terminal_probe = TerminalProbe()
        self.results: list[CheckResult] = []

    def run(self, verbose: bool = False, auto_fix: bool = False) -> list[CheckResult]:
        """
        Run all diagnostic checks.

        Args:
            verbose: Show detailed output
            auto_fix: Attempt to fix issues automatically

        Returns:
            List of check results
        """
        self.results = []

        # Run all checks
        self._check_shell()
        self._check_terminal()
        self._check_colors()
        self._check_fonts()
        self._check_git()
        self._check_starship()
        self._check_nerd_fonts()
        self._check_system()

        if verbose:
            self._display_detailed_results()
        else:
            self._display_summary()

        return self.results

    def _check_shell(self) -> None:
        """Check shell configuration."""
        try:
            shell_info = self.shell_detector.detect()

            if shell_info.shell_type == ShellType.UNKNOWN:
                self.results.append(
                    CheckResult(
                        name="Shell Detection",
                        status=CheckStatus.WARNING,
                        message="Unknown shell detected",
                        details=f"Shell: {shell_info.version}",
                        recommendation="Consider using bash, zsh, or fish",
                    )
                )
            else:
                status_str = (
                    f"{shell_info.shell_type.value} {shell_info.version}"
                )
                self.results.append(
                    CheckResult(
                        name="Shell Detection",
                        status=CheckStatus.OK,
                        message=status_str,
                        details=f"Config: {shell_info.config_path}",
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name="Shell Detection",
                    status=CheckStatus.ERROR,
                    message=f"Error detecting shell: {e}",
                )
            )

    def _check_terminal(self) -> None:
        """Check terminal emulator."""
        try:
            terminal_info = self.terminal_probe.detect()

            details = [
                f"Emulator: {terminal_info.name}",
                f"Size: {terminal_info.columns}x{terminal_info.rows}",
            ]

            if terminal_info.version:
                details.append(f"Version: {terminal_info.version}")

            self.results.append(
                CheckResult(
                    name="Terminal Emulator",
                    status=CheckStatus.OK,
                    message=terminal_info.name,
                    details="\n".join(details),
                )
            )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name="Terminal Emulator",
                    status=CheckStatus.WARNING,
                    message=f"Error detecting terminal: {e}",
                )
            )

    def _check_colors(self) -> None:
        """Check color support."""
        try:
            terminal_info = self.terminal_probe.detect()

            if terminal_info.supports_true_color:
                self.results.append(
                    CheckResult(
                        name="Color Support",
                        status=CheckStatus.OK,
                        message="True color (24-bit) supported",
                        details="Full RGB color support available",
                    )
                )
            elif terminal_info.supports_256_color:
                self.results.append(
                    CheckResult(
                        name="Color Support",
                        status=CheckStatus.OK,
                        message="256 colors supported",
                        details="Good color support",
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name="Color Support",
                        status=CheckStatus.WARNING,
                        message="Limited color support",
                        details="Only basic colors available",
                        recommendation="Consider using a modern terminal emulator",
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name="Color Support",
                    status=CheckStatus.ERROR,
                    message=f"Error checking colors: {e}",
                )
            )

    def _check_fonts(self) -> None:
        """Check font configuration."""
        try:
            terminal_info = self.terminal_probe.detect()

            if terminal_info.font_name:
                self.results.append(
                    CheckResult(
                        name="Font",
                        status=CheckStatus.OK,
                        message=terminal_info.font_name,
                        details=f"Size: {terminal_info.font_size}pt"
                        if terminal_info.font_size
                        else None,
                    )
                )
            else:
                self.results.append(
                    CheckResult(
                        name="Font",
                        status=CheckStatus.OK,
                        message="Font configured",
                        details="Unable to detect specific font",
                    )
                )
        except Exception as e:
            self.results.append(
                CheckResult(
                    name="Font",
                    status=CheckStatus.WARNING,
                    message=f"Error checking font: {e}",
                )
            )

    def _check_git(self) -> None:
        """Check git installation."""
        git_path = shutil.which("git")

        if git_path:
            try:
                result = subprocess.run(
                    ["git", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                version = result.stdout.strip()
                self.results.append(
                    CheckResult(
                        name="Git",
                        status=CheckStatus.OK,
                        message=version,
                        details=f"Path: {git_path}",
                    )
                )
            except Exception:
                self.results.append(
                    CheckResult(
                        name="Git",
                        status=CheckStatus.OK,
                        message="Git installed",
                        details=f"Path: {git_path}",
                    )
                )
        else:
            self.results.append(
                CheckResult(
                    name="Git",
                    status=CheckStatus.WARNING,
                    message="Git not found",
                    recommendation="Install git for git branch display in prompts",
                )
            )

    def _check_starship(self) -> None:
        """Check starship installation."""
        starship_path = shutil.which("starship")

        if starship_path:
            try:
                result = subprocess.run(
                    ["starship", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                version = result.stdout.strip()
                self.results.append(
                    CheckResult(
                        name="Starship",
                        status=CheckStatus.OK,
                        message=version,
                    )
                )
            except Exception:
                self.results.append(
                    CheckResult(
                        name="Starship",
                        status=CheckStatus.OK,
                        message="Starship installed",
                    )
                )
        else:
            self.results.append(
                CheckResult(
                    name="Starship",
                    status=CheckStatus.WARNING,
                    message="Starship not installed",
                    details="Optional: Advanced prompt customization",
                    recommendation="curl -sS https://starship.rs/install.sh | sh",
                )
            )

    def _check_nerd_fonts(self) -> None:
        """Check Nerd Font installation."""
        # Check common Nerd Font locations
        nerd_font_paths = [
            Path.home() / ".local" / "share" / "fonts",
            Path.home() / ".fonts",
            Path("/usr/share/fonts"),
            Path("/Library/Fonts"),  # macOS
        ]

        nerd_fonts_found = []

        for font_dir in nerd_font_paths:
            if font_dir.exists():
                # Look for Nerd Font files
                for font_file in font_dir.rglob("*Nerd Font*"):
                    if font_file.suffix in [".ttf", ".otf"]:
                        nerd_fonts_found.append(font_file.name)
                        break

        # Check environment variables
        if "NERDFONT" in str(Path.home()):
            nerd_fonts_found.append("NERDFONT environment variable set")

        if nerd_fonts_found:
            self.results.append(
                CheckResult(
                    name="Nerd Fonts",
                    status=CheckStatus.OK,
                    message=f"Found {len(nerd_fonts_found)} Nerd Font(s)",
                    details="\n".join(nerd_fonts_found[:5]),
                )
            )
        else:
            self.results.append(
                CheckResult(
                    name="Nerd Fonts",
                    status=CheckStatus.WARNING,
                    message="Nerd Fonts not detected",
                    details="Some theme icons may not display correctly",
                    recommendation="https://www.nerdfonts.com/font-downloads",
                )
            )

    def _check_system(self) -> None:
        """Check system information."""
        import os
        import platform

        details = [
            f"OS: {platform.system()} {platform.release()}",
            f"Arch: {platform.machine()}",
            f"Home: {Path.home()}",
            f"Python: {platform.python_version()}",
        ]

        self.results.append(
            CheckResult(
                name="System Info",
                status=CheckStatus.OK,
                message=f"{platform.system()} {platform.release()}",
                details="\n".join(details),
            )
        )

    def _display_detailed_results(self) -> None:
        """Display detailed results."""
        for result in self.results:
            icon = self._get_status_icon(result.status)
            console.print(f"\n{icon} [bold]{result.name}[/bold]: {result.message}")

            if result.details:
                console.print(f"  [dim]{result.details}[/dim]")

            if result.recommendation:
                console.print(f"  [yellow]→ {result.recommendation}[/yellow]")

    def _display_summary(self) -> None:
        """Display summary table."""
        table = Table(title="clicool doctor")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="dim")

        ok_count = 0
        warning_count = 0
        error_count = 0

        for result in self.results:
            icon = self._get_status_icon(result.status)
            status_style = self._get_status_style(result.status)

            table.add_row(
                result.name,
                f"{icon} {result.message}",
                result.details or "",
                style=status_style,
            )

            if result.status == CheckStatus.OK:
                ok_count += 1
            elif result.status == CheckStatus.WARNING:
                warning_count += 1
            elif result.status == CheckStatus.ERROR:
                error_count += 1

        console.print(table)

        # Summary
        summary = f"\n[bold]Summary:[/bold] {ok_count} passed, {warning_count} warnings, {error_count} errors"
        console.print(summary)

        # Show recommendations if any
        recommendations = [
            r.recommendation for r in self.results if r.recommendation
        ]
        if recommendations:
            console.print(
                Panel(
                    "\n".join(f"• {r}" for r in recommendations),
                    title="Recommendations",
                    border_style="yellow",
                )
            )

    def _get_status_icon(self, status: CheckStatus) -> str:
        """Get icon for status."""
        icons = {
            CheckStatus.OK: "✔",
            CheckStatus.WARNING: "⚠",
            CheckStatus.ERROR: "✘",
            CheckStatus.SKIPPED: "○",
        }
        return icons.get(status, "?")

    def _get_status_style(self, status: CheckStatus) -> str:
        """Get style for status."""
        styles = {
            CheckStatus.OK: "green",
            CheckStatus.WARNING: "yellow",
            CheckStatus.ERROR: "red",
            CheckStatus.SKIPPED: "dim",
        }
        return styles.get(status, "")

    def get_summary(self) -> dict:
        """Get summary of results."""
        return {
            "ok": sum(1 for r in self.results if r.status == CheckStatus.OK),
            "warning": sum(1 for r in self.results if r.status == CheckStatus.WARNING),
            "error": sum(1 for r in self.results if r.status == CheckStatus.ERROR),
            "skipped": sum(1 for r in self.results if r.status == CheckStatus.SKIPPED),
            "total": len(self.results),
        }


# Singleton instance
_doctor = Doctor()


def run_doctor(verbose: bool = False, auto_fix: bool = False) -> list[CheckResult]:
    """Run doctor diagnostics."""
    return _doctor.run(verbose, auto_fix)


__all__ = [
    "CheckStatus",
    "CheckResult",
    "Doctor",
    "run_doctor",
]
