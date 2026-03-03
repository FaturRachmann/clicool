"""Color utilities for terminal output."""


class ColorConverter:
    """Convert between color formats."""

    # ANSI color codes
    ANSI_COLORS = {
        "black": 30,
        "red": 31,
        "green": 32,
        "yellow": 33,
        "blue": 34,
        "magenta": 35,
        "cyan": 36,
        "white": 37,
    }

    # Bright ANSI colors
    BRIGHT_COLORS = {
        "bright_black": 90,
        "bright_red": 91,
        "bright_green": 92,
        "bright_yellow": 93,
        "bright_blue": 94,
        "bright_magenta": 95,
        "bright_cyan": 96,
        "bright_white": 97,
    }

    @staticmethod
    def hex_to_rgb(hex_color: str) -> tuple[int, ...]:
        """
        Convert hex color to RGB tuple.

        Args:
            hex_color: Hex color string (#RRGGBB or RRGGBB)

        Returns:
            Tuple of (R, G, B) values
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) != 6:
            raise ValueError(f"Invalid hex color: {hex_color}")

        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_ansi(r: int, g: int, b: int) -> int:
        """
        Convert RGB to nearest ANSI color code.

        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)

        Returns:
            ANSI color code
        """
        # Simple conversion to nearest ANSI color
        # This is a basic implementation
        if r == g == b:
            # Grayscale
            if r < 128:
                return 30  # Black
            return 37  # White

        # Find dominant color
        max_val = max(r, g, b)
        if max_val == r:
            return 31  # Red
        elif max_val == g:
            return 32  # Green
        return 34  # Blue

    @staticmethod
    def rgb_to_256(r: int, g: int, b: int) -> int:
        """
        Convert RGB to 256-color code.

        Args:
            r: Red value (0-255)
            g: Green value (0-255)
            b: Blue value (0-255)

        Returns:
            256-color code (0-255)
        """
        # Convert to 6x6x6 color cube
        r_idx = int(r / 256 * 6)
        g_idx = int(g / 256 * 6)
        b_idx = int(b / 256 * 6)

        # Clamp values
        r_idx = min(5, max(0, r_idx))
        g_idx = min(5, max(0, g_idx))
        b_idx = min(5, max(0, b_idx))

        # Calculate 256-color code (16-231 are color cube)
        return 16 + 36 * r_idx + 6 * g_idx + b_idx

    @staticmethod
    def hex_to_ansi_escape(hex_color: str, bright: bool = False) -> str:
        """
        Convert hex color to ANSI escape sequence.

        Args:
            hex_color: Hex color string
            bright: Use bright variant

        Returns:
            ANSI escape sequence
        """
        r, g, b = ColorConverter.hex_to_rgb(hex_color)
        return f"\033[38;2;{r}:{g}:{b}m"

    @staticmethod
    def named_to_ansi(name: str) -> int | None:
        """
        Convert color name to ANSI code.

        Args:
            name: Color name

        Returns:
            ANSI color code or None
        """
        name = name.lower().strip()

        if name in ColorConverter.ANSI_COLORS:
            return ColorConverter.ANSI_COLORS[name]
        if name in ColorConverter.BRIGHT_COLORS:
            return ColorConverter.BRIGHT_COLORS[name]

        return None


class ColorPalette:
    """Predefined color palettes."""

    CYBERPUNK = {
        "background": "#0d1117",
        "foreground": "#c9d1d9",
        "cyan": "#00ffff",
        "magenta": "#ff00ff",
        "yellow": "#ffff00",
        "green": "#00ff00",
        "red": "#ff5555",
        "blue": "#5050ff",
    }

    MATRIX = {
        "background": "#000000",
        "foreground": "#00ff00",
        "green": "#00ff00",
        "dark_green": "#003300",
    }

    RETRO = {
        "background": "#1a1a1a",
        "foreground": "#ffb000",
        "amber": "#ffb000",
        "dark_amber": "#cc8800",
    }

    MINIMAL = {
        "background": "#ffffff",
        "foreground": "#333333",
        "gray": "#666666",
        "blue": "#0066cc",
    }

    DEVOPS = {
        "background": "#0f172a",
        "foreground": "#e2e8f0",
        "blue": "#38bdf8",
        "green": "#4ade80",
        "yellow": "#facc15",
        "purple": "#c084fc",
    }


__all__ = ["ColorConverter", "ColorPalette"]
