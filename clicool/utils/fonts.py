"""Font detection utilities."""

import os
from pathlib import Path


class FontDetector:
    """Detect installed fonts."""

    # Common font directories
    FONT_DIRS = [
        Path.home() / ".local" / "share" / "fonts",
        Path.home() / ".fonts",
        Path("/usr/share/fonts"),
        Path("/usr/local/share/fonts"),
        Path("/Library/Fonts"),  # macOS
        Path("/System/Library/Fonts"),  # macOS
        Path(os.environ.get("WINDIR", "C:\\Windows")) / "Fonts",  # Windows
    ]

    # Nerd Font patterns
    NERD_FONT_PATTERNS = [
        "Nerd Font",
        "NF",
        "Mono Nerd Font",
    ]

    # Recommended fonts for terminal
    RECOMMENDED_FONTS = [
        "JetBrainsMono Nerd Font",
        "Fira Code Nerd Font",
        "Hack Nerd Font",
        "Source Code Pro",
        "Monospace",
        "Cascadia Code",
    ]

    def detect_fonts(self) -> list[str]:
        """
        Detect installed fonts.

        Returns:
            List of font family names
        """
        fonts = []

        for font_dir in self.FONT_DIRS:
            if font_dir.exists():
                fonts.extend(self._scan_font_directory(font_dir))

        return sorted(set(fonts))

    def detect_nerd_fonts(self) -> list[str]:
        """
        Detect installed Nerd Fonts.

        Returns:
            List of Nerd Font family names
        """
        all_fonts = self.detect_fonts()
        nerd_fonts = []

        for font in all_fonts:
            if self._is_nerd_font(font):
                nerd_fonts.append(font)

        return nerd_fonts

    def is_nerd_font_installed(self) -> bool:
        """
        Check if any Nerd Font is installed.

        Returns:
            True if Nerd Font found
        """
        return len(self.detect_nerd_fonts()) > 0

    def get_recommended_font(self) -> str | None:
        """
        Get first recommended font that is installed.

        Returns:
            Recommended font name or None
        """
        installed_fonts = self.detect_fonts()

        for recommended in self.RECOMMENDED_FONTS:
            for installed in installed_fonts:
                if recommended.lower() in installed.lower():
                    return installed

        return None

    def _scan_font_directory(self, directory: Path) -> list[str]:
        """
        Scan directory for font files.

        Args:
            directory: Directory to scan

        Returns:
            List of font names
        """
        fonts: list[str] = []

        if not directory.exists():
            return fonts

        # Font file extensions
        font_extensions = {".ttf", ".otf", ".ttc", ".pfb"}

        for font_file in directory.rglob("*"):
            if font_file.suffix.lower() in font_extensions:
                # Extract font name from filename
                font_name = self._extract_font_name(font_file)
                if font_name:
                    fonts.append(font_name)

        return fonts

    def _extract_font_name(self, font_file: Path) -> str | None:
        """
        Extract font name from file.

        Args:
            font_file: Path to font file

        Returns:
            Font name or None
        """
        # Simple extraction from filename
        # A full implementation would read font metadata
        name = font_file.stem

        # Remove common suffixes
        for suffix in ["Regular", "Bold", "Italic", "Light", "Medium"]:
            name = name.replace(suffix, "")

        # Clean up
        name = name.replace("-", " ").replace("_", " ").strip()

        return name if name else None

    def _is_nerd_font(self, font_name: str) -> bool:
        """
        Check if font is a Nerd Font.

        Args:
            font_name: Font name

        Returns:
            True if Nerd Font
        """
        font_lower = font_name.lower()

        for pattern in self.NERD_FONT_PATTERNS:
            if pattern.lower() in font_lower:
                return True

        return False

    def get_font_info(self) -> dict:
        """
        Get comprehensive font information.

        Returns:
            Dictionary with font information
        """
        all_fonts = self.detect_fonts()
        nerd_fonts = self.detect_nerd_fonts()
        recommended = self.get_recommended_font()

        return {
            "total_fonts": len(all_fonts),
            "nerd_fonts": nerd_fonts,
            "has_nerd_font": len(nerd_fonts) > 0,
            "recommended_installed": recommended is not None,
            "recommended_font": recommended,
        }


# Singleton instance
_detector = FontDetector()


def detect_fonts() -> list[str]:
    """Detect installed fonts."""
    return _detector.detect_fonts()


def detect_nerd_fonts() -> list[str]:
    """Detect installed Nerd Fonts."""
    return _detector.detect_nerd_fonts()


def is_nerd_font_installed() -> bool:
    """Check if Nerd Font is installed."""
    return _detector.is_nerd_font_installed()


__all__ = [
    "FontDetector",
    "detect_fonts",
    "detect_nerd_fonts",
    "is_nerd_font_installed",
]
