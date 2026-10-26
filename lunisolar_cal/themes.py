"""Qt themes using Catppuccin's MIT-licensed color palette.

Palette source: https://github.com/catppuccin/palette/blob/main/palette.json
Palette copyright (c) 2021 Catppuccin; see licenses/catppuccin-MIT.txt.
"""

from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPalette


NATIVE_SCHEMES = (
    Qt.ColorScheme.Unknown,
    Qt.ColorScheme.Light,
    Qt.ColorScheme.Dark,
)
CATPPUCCIN_FLAVORS = ("latte", "frappe", "macchiato", "mocha")

CATPPUCCIN_COLORS = {
    "latte": {
        "base": "#eff1f5",
        "mantle": "#e6e9ef",
        "crust": "#dce0e8",
        "surface0": "#ccd0da",
        "surface1": "#bcc0cc",
        "surface2": "#acb0be",
        "overlay0": "#9ca0b0",
        "subtext0": "#6c6f85",
        "subtext1": "#5c5f77",
        "text": "#4c4f69",
        "mauve": "#8839ef",
        "blue": "#1e66f5",
        "red": "#d20f39",
        "border": "#7c7f93",
    },
    "frappe": {
        "base": "#303446",
        "mantle": "#292c3c",
        "crust": "#232634",
        "surface0": "#414559",
        "surface1": "#51576d",
        "surface2": "#626880",
        "overlay0": "#737994",
        "subtext0": "#a5adce",
        "subtext1": "#b5bfe2",
        "text": "#c6d0f5",
        "mauve": "#ca9ee6",
        "blue": "#8caaee",
        "red": "#e78284",
        "border": "#737994",
    },
    "macchiato": {
        "base": "#24273a",
        "mantle": "#1e2030",
        "crust": "#181926",
        "surface0": "#363a4f",
        "surface1": "#494d64",
        "surface2": "#5b6078",
        "overlay0": "#6e738d",
        "subtext0": "#a5adcb",
        "subtext1": "#b8c0e0",
        "text": "#cad3f5",
        "mauve": "#c6a0f6",
        "blue": "#8aadf4",
        "red": "#ed8796",
        "border": "#6e738d",
    },
    "mocha": {
        "base": "#1e1e2e",
        "mantle": "#181825",
        "crust": "#11111b",
        "surface0": "#313244",
        "surface1": "#45475a",
        "surface2": "#585b70",
        "overlay0": "#6c7086",
        "subtext0": "#a6adc8",
        "subtext1": "#bac2de",
        "text": "#cdd6f4",
        "mauve": "#cba6f7",
        "blue": "#89b4fa",
        "red": "#f38ba8",
        "border": "#6c7086",
    },
}


def make_palette(colors, base_palette):
    """Apply the same role mapping to every Catppuccin flavor."""
    palette = QPalette(base_palette)
    roles = {
        QPalette.ColorRole.Window: "base",
        QPalette.ColorRole.WindowText: "text",
        QPalette.ColorRole.Base: "mantle",
        QPalette.ColorRole.AlternateBase: "base",
        QPalette.ColorRole.Text: "text",
        QPalette.ColorRole.Button: "surface0",
        QPalette.ColorRole.ButtonText: "text",
        QPalette.ColorRole.ToolTipBase: "surface0",
        QPalette.ColorRole.ToolTipText: "text",
        QPalette.ColorRole.Light: "surface1",
        QPalette.ColorRole.Midlight: "surface1",
        QPalette.ColorRole.Dark: "surface2",
        QPalette.ColorRole.Mid: "border",
        QPalette.ColorRole.Shadow: "crust",
        QPalette.ColorRole.Highlight: "mauve",
        QPalette.ColorRole.HighlightedText: "base",
        QPalette.ColorRole.Link: "blue",
        QPalette.ColorRole.LinkVisited: "mauve",
        QPalette.ColorRole.BrightText: "red",
        QPalette.ColorRole.PlaceholderText: "subtext0",
        QPalette.ColorRole.Accent: "mauve",
    }
    for role, name in roles.items():
        palette.setColor(role, QColor(colors[name]))
    for role in (
        QPalette.ColorRole.WindowText,
        QPalette.ColorRole.Text,
        QPalette.ColorRole.ButtonText,
        QPalette.ColorRole.PlaceholderText,
    ):
        palette.setColor(QPalette.ColorGroup.Disabled, role, QColor(colors["overlay0"]))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Highlight,
                     QColor(colors["surface1"]))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.HighlightedText,
                     QColor(colors["overlay0"]))
    return palette


def tint_icon(icon, color, size):
    """Keep the existing icon's shape and match the accent button text."""
    pixmap = icon.pixmap(size)
    painter = QPainter(pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return QIcon(pixmap)


class ThemeController:
    def __init__(self, app, primary_button, result_panel):
        self.app = app
        self.primary_button = primary_button
        self.result_panel = result_panel
        self.native_style = app.style().objectName()
        self.native_icon = QIcon(primary_button.icon())
        self.native_panel_role = result_panel.backgroundRole()
        self.native_panel_fill = result_panel.autoFillBackground()
        self._custom = False

    def apply(self, index):
        if not 0 <= index < len(NATIVE_SCHEMES) + len(CATPPUCCIN_FLAVORS):
            raise ValueError("Unknown theme index.")
        if index < len(NATIVE_SCHEMES):
            if self._custom:
                self.app.setPalette(QPalette())
                self.app.setStyle(self.native_style)
            self.app.styleHints().setColorScheme(NATIVE_SCHEMES[index])
            self.primary_button.setPalette(QPalette())
            self.primary_button.setIcon(self.native_icon)
            self.result_panel.setBackgroundRole(self.native_panel_role)
            self.result_panel.setAutoFillBackground(self.native_panel_fill)
            self._custom = False
            return

        flavor = CATPPUCCIN_FLAVORS[index - len(NATIVE_SCHEMES)]
        colors = CATPPUCCIN_COLORS[flavor]
        scheme = Qt.ColorScheme.Light if flavor == "latte" else Qt.ColorScheme.Dark
        self.app.styleHints().setColorScheme(scheme)
        if not self._custom:
            self.app.setStyle("Fusion")
        palette = make_palette(colors, self.app.palette())
        self.app.setPalette(palette)
        self.result_panel.setBackgroundRole(QPalette.ColorRole.Base)
        self.result_panel.setAutoFillBackground(True)

        button_palette = QPalette(palette)
        for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive):
            button_palette.setColor(group, QPalette.ColorRole.Button, QColor(colors["mauve"]))
            button_palette.setColor(group, QPalette.ColorRole.ButtonText, QColor(colors["base"]))
        self.primary_button.setPalette(button_palette)
        self.primary_button.setIcon(tint_icon(
            self.native_icon, QColor(colors["base"]), self.primary_button.iconSize(),
        ))
        self._custom = True
