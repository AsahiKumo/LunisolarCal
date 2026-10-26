"""Theme integration checks; widgets stay hidden throughout the tests."""

import unittest

from PySide6.QtCore import QCoreApplication, QEvent, QEventLoop, QTimer
from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

from lunisolar_cal.gui import LsConvWindow


class ThemeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])
        cls.app.setQuitOnLastWindowClosed(False)
        cls.native_style = cls.app.style().objectName()

    @staticmethod
    def settle():
        loop = QEventLoop()
        QTimer.singleShot(25, loop.quit)
        loop.exec()

    def setUp(self):
        self.app.setPalette(QPalette())
        self.app.setStyle(self.native_style)
        self.app.styleHints().unsetColorScheme()
        self.settle()
        self.window = LsConvWindow()
        self.ui = self.window.ui
        self.ui.langCombo.setCurrentIndex(0)
        self.original_icon_key = self.ui.convButton.icon().cacheKey()
        self.original_panel_role = self.ui.resultLabel.backgroundRole()
        self.original_panel_fill = self.ui.resultLabel.autoFillBackground()

    def tearDown(self):
        self.window.close()
        self.window.deleteLater()
        QCoreApplication.sendPostedEvents(None, QEvent.Type.DeferredDelete)
        self.app.setPalette(QPalette())
        self.app.setStyle(self.native_style)
        self.app.styleHints().unsetColorScheme()
        self.settle()

    def select_theme(self, index):
        self.ui.themeCombo.setCurrentIndex(index)
        self.settle()
        self.assertFalse(self.window.isVisible())

    def palette_signature(self):
        palette = self.app.palette()
        return tuple(
            palette.color(group, role).rgba()
            for group in (QPalette.ColorGroup.Active, QPalette.ColorGroup.Inactive,
                          QPalette.ColorGroup.Disabled)
            for role in (QPalette.ColorRole.Window, QPalette.ColorRole.Text,
                         QPalette.ColorRole.Base, QPalette.ColorRole.Button,
                         QPalette.ColorRole.ButtonText, QPalette.ColorRole.Highlight)
        )

    def conversion_state(self):
        return (
            self.ui.calCombo.currentIndex(), self.ui.yearSpin.value(),
            self.ui.monthSpin.value(), self.ui.daySpin.value(),
            self.ui.leapCheck.isChecked(), self.ui.chineseCheck.isChecked(),
            self.ui.resultLabel.text(), self.window._copy_text,
            self.ui.copyButton.isEnabled(),
        )

    def test_all_four_flavors_apply_distinct_palettes_and_accent_buttons(self):
        expected = (
            (3, "#eff1f5", "#4c4f69", "#8839ef"),
            (4, "#303446", "#c6d0f5", "#ca9ee6"),
            (5, "#24273a", "#cad3f5", "#c6a0f6"),
            (6, "#1e1e2e", "#cdd6f4", "#cba6f7"),
        )
        self.assertEqual(self.ui.themeCombo.count(), 7)
        for index, background, text, accent in expected:
            with self.subTest(index=index):
                self.select_theme(index)
                palette = self.app.palette()
                self.assertEqual(self.app.style().objectName(), "fusion")
                self.assertEqual(palette.window().color().name(), background)
                self.assertEqual(palette.text().color().name(), text)
                self.assertEqual(palette.highlight().color().name(), accent)
                self.assertEqual(self.ui.resultLabel.backgroundRole(), QPalette.ColorRole.Base)
                self.assertTrue(self.ui.resultLabel.autoFillBackground())
                button = self.ui.convButton
                self.assertEqual(button.palette().button().color().name(), accent)
                self.assertEqual(button.palette().buttonText().color().name(), background)
                self.assertFalse(button.icon().isNull())

    def test_every_custom_to_native_transition_restores_original_palette_and_icon(self):
        native = {}
        for index in range(3):
            self.select_theme(index)
            native[index] = self.palette_signature()
        for custom in range(3, 7):
            for index in range(3):
                with self.subTest(custom=custom, native=index):
                    self.select_theme(custom)
                    self.select_theme(index)
                    self.assertEqual(self.app.style().objectName(), self.native_style)
                    self.assertEqual(self.palette_signature(), native[index])
                    self.assertEqual(self.app.palette().resolveMask(), 0)
                    self.assertEqual(self.ui.convButton.palette().resolveMask(), 0)
                    self.assertEqual(self.ui.convButton.icon().cacheKey(), self.original_icon_key)
                    self.assertEqual(self.ui.resultLabel.backgroundRole(), self.original_panel_role)
                    self.assertEqual(self.ui.resultLabel.autoFillBackground(), self.original_panel_fill)

    def test_switching_themes_preserves_results_errors_and_leap_month_input(self):
        cases = (
            (0, 2024, 2, 10, False, True),
            (0, 2024, 2, 30, False, False),
            (1, 2023, 2, 1, True, True),
        )
        for calendar, year, month, day, leap, valid in cases:
            self.ui.calCombo.setCurrentIndex(calendar)
            self.ui.yearSpin.setValue(year)
            self.ui.monthSpin.setValue(month)
            self.ui.daySpin.setValue(day)
            self.ui.leapCheck.setChecked(leap)
            self.window.on_convert_clicked()
            self.assertEqual(self.ui.copyButton.isEnabled(), valid)
            state = self.conversion_state()
            for index in (3, 4, 5, 6, 1, 2, 0):
                with self.subTest(calendar=calendar, valid=valid, theme=index):
                    self.select_theme(index)
                    self.assertEqual(self.conversion_state(), state)

    def test_language_switch_keeps_theme_and_translates_the_four_options(self):
        self.select_theme(5)
        colors = self.palette_signature()
        self.ui.langCombo.setCurrentIndex(1)
        self.settle()
        self.assertEqual(self.ui.themeCombo.currentIndex(), 5)
        self.assertEqual(self.palette_signature(), colors)
        self.assertEqual(
            [self.ui.themeCombo.itemText(i) for i in range(3, 7)],
            ["Latte (Light)", "Frappé (Dark)", "Macchiato (Dark)", "Mocha (Dark)"],
        )
        self.ui.langCombo.setCurrentIndex(0)
        self.settle()
        self.assertEqual(self.ui.themeCombo.currentIndex(), 5)
        self.assertEqual(self.palette_signature(), colors)
