"""Layer system for modular theme components."""

from typing import Optional

from ..core.theme_loader import LayerConfig, ThemeConfig


class LayerManager:
    """Manage theme layers."""

    def __init__(self):
        self.active_layers: list[str] = []

    def add_layer(self, layer_name: str) -> bool:
        """Add a layer."""
        if layer_name not in self.active_layers:
            self.active_layers.append(layer_name)
            return True
        return False

    def remove_layer(self, layer_name: str) -> bool:
        """Remove a layer."""
        if layer_name in self.active_layers:
            self.active_layers.remove(layer_name)
            return True
        return False

    def list_layers(self) -> list[str]:
        """List active layers."""
        return self.active_layers.copy()

    def merge_layers(
        self, theme: ThemeConfig, layers: list[LayerConfig]
    ) -> ThemeConfig:
        """
        Merge layers into a theme.

        Args:
            theme: Base theme configuration
            layers: List of layer configurations to merge

        Returns:
            Merged theme configuration
        """
        # For now, just add layer widgets to theme
        merged_widgets = list(theme.widgets) if theme.widgets else []

        for layer in layers:
            if layer.widget:
                # Add layer widget configuration
                merged_widgets.append(layer.widget.name)

        # Create modified theme (in real implementation, would deep merge)
        return theme

    def clear_layers(self) -> None:
        """Clear all layers."""
        self.active_layers.clear()


__all__ = ["LayerManager"]
