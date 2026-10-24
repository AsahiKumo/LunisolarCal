import sys
from datetime import date
from pathlib import Path
from PySide6.QtCore import Qt, QTimer, QTranslator, QCoreApplication, QLocale, QUrl
from PySide6.QtWidgets import QApplication, QWidget, QMessageBox, QDialog, QVBoxLayout, QComboBox, QTextBrowser, QPushButton
from PySide6.QtGui import QDesktopServices, QKeySequence, QShortcut
from .ui_converter import Ui_LsConvWindow
from . import (
    __version__,
    MIN_INPUT_YEAR,
    MAX_INPUT_YEAR,
    solar_to_lunisolar,
    lunisolar_to_solar,
)
from .formatting import format_lunisolar, format_solar, format_calendar_error

class LsConvWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_LsConvWindow()
        self.ui.setupUi(self)
        self._translator = QTranslator(self)
        self._copy_text = ""
        self._copy_timer = QTimer(self)
        self._copy_timer.setSingleShot(True)
        self._copy_timer.timeout.connect(
            lambda: self.ui.copyButton.setText(self.tr("复制结果"))
        )
        self.ui.copyButton.clicked.connect(self.on_copy_clicked)
        self.ui.yearSpin.setRange(MIN_INPUT_YEAR, MAX_INPUT_YEAR)
        self.ui.todayButton.clicked.connect(self.on_today_clicked)
        self.ui.convButton.clicked.connect(self.on_convert_clicked)
        self.ui.aboutButton.clicked.connect(self.on_about_clicked)
        self.ui.calCombo.currentIndexChanged.connect(self.on_calendar_changed)
        self.on_calendar_changed(self.ui.calCombo.currentIndex())
        self.ui.yearSpin.valueChanged.connect(self.on_input_changed)
        self.ui.monthSpin.valueChanged.connect(self.on_input_changed)
        self.ui.daySpin.valueChanged.connect(self.on_input_changed)
        self.ui.leapCheck.toggled.connect(self.on_input_changed)
        self.ui.chineseCheck.toggled.connect(self.on_input_changed)
        self.setup_keyboard()
        self.ui.langCombo.currentIndexChanged.connect(
            self.on_language_changed
        )
        self.on_language_changed(self.ui.langCombo.currentIndex())
    
    def setup_keyboard(self):
        self._shortcuts = []
        for key, button in [
            ("Return", self.ui.convButton),
            ("Enter", self.ui.convButton),
            ("Alt+T", self.ui.todayButton),
            ("Ctrl+Shift+C", self.ui.copyButton),
        ]:
            shortcut = QShortcut(QKeySequence(key), self)
            shortcut.setAutoRepeat(False)
            shortcut.activated.connect(button.click)
            self._shortcuts.append(shortcut)
        self.ui.yearSpin.setFocus()
        self.ui.yearSpin.selectAll()
    
    def on_convert_clicked(self):
        for spin in (self.ui.yearSpin, self.ui.monthSpin, self.ui.daySpin):
            spin.interpretText()
        mode = self.ui.calCombo.currentIndex()
        year = self.ui.yearSpin.value()
        month = self.ui.monthSpin.value()
        day = self.ui.daySpin.value()
        is_leap = self.ui.leapCheck.isChecked()
        try:
            if mode == 0:
                result = solar_to_lunisolar(year, month, day)
                text = format_lunisolar(
                    result,
                    chinese=self.ui.chineseCheck.isChecked(),
                    translate=QCoreApplication.translate,
                )
            else:
                result = lunisolar_to_solar(
                    year, month, day, is_leap=is_leap
                )
                text = format_solar(
                    result,
                    translate=QCoreApplication.translate,
                )
        except ValueError as exc:
            text = format_calendar_error(
                exc,
                translate=QCoreApplication.translate,
            )
            self._copy_text = ""
        else:
            self._copy_text = text
        self._copy_timer.stop()
        self.ui.resultLabel.setText(text)
        self.ui.copyButton.setText(self.tr("复制结果"))
        self.ui.copyButton.setEnabled(bool(self._copy_text))
    
    def on_today_clicked(self):
        today = date.today()
        if self.ui.calCombo.currentIndex() == 0:
            year, month, day = today.year, today.month, today.day
            is_leap = False
        else:
            lunar = solar_to_lunisolar(today.year, today.month, today.day)
            year, month, day = lunar.year, lunar.month, lunar.day
            is_leap = lunar.is_leap
        self.ui.yearSpin.setValue(year)
        self.ui.monthSpin.setValue(month)
        self.ui.daySpin.setValue(day)
        self.ui.leapCheck.setChecked(is_leap)
        self.on_convert_clicked()
    
    def on_copy_clicked(self):
        if not self._copy_text:
            return
        QApplication.clipboard().setText(self._copy_text)
        self.ui.copyButton.setText(self.tr("已复制"))
        self._copy_timer.start(1200)
    
    def on_input_changed(self, _value=None):
        self._copy_text = ""
        self._copy_timer.stop()
        self.ui.resultLabel.setText(self.tr("等待转换"))
        self.ui.copyButton.setEnabled(False)
        self.ui.copyButton.setText(self.tr("复制结果"))
    
    def on_calendar_changed(self, index):
        is_lunar = index == 1
        self.ui.chineseCheck.setEnabled(not is_lunar)
        self.ui.leapCheck.setEnabled(is_lunar)
        if not is_lunar:
            self.ui.leapCheck.setChecked(False)
        self.on_input_changed()
    
    def system_language_index(self):
        for tag in QLocale.system().uiLanguages():
            language = tag.replace("_", "-").split("-", 1)[0].lower()
            if language == "zh":
                return 0
            if language == "en":
                return 1
        return 1
    
    def on_language_changed(self, index):
        app = QApplication.instance()
        target_index = self.system_language_index() if index == 2 else index
        if target_index == 1:
            qm_path = Path(__file__).resolve().parent / "i18n" / "app_en.qm"
            if not self._translator.load(str(qm_path)):
                self.ui.langCombo.setCurrentIndex(0)
                QMessageBox.warning(
                    self, "加载失败",
                    f"无法加载英文翻译文件：\n{qm_path}"
                )
                return
            app.installTranslator(self._translator)
        else:
            app.removeTranslator(self._translator)
        self.ui.retranslateUi(self)
        self.on_input_changed()
    
    def on_about_clicked(self):
        text = self.tr(
            "<h3>公农历转换</h3>"
            "<p>版本：{version}<br>作者：朝曦凝云AsahiKumo<br>项目许可证：MIT</p>"
            "<p>基于 sxtwl 的公历、农历双向转换工具。</p>"
            "<p>开发中使用 OpenAI Codex 辅助编程、调试、文档整理和图标制作。</p>"
            '<p><a href="https://github.com/AsahiKumo/LunisolarCal">项目主页</a></p>'
        ).format(version=__version__)
        box = QMessageBox(self)
        box.setWindowTitle(self.tr("关于"))
        box.setText(text)
        box.setIconPixmap(self.windowIcon().pixmap(64, 64))
        ok_button = box.addButton(self.tr("确定"), QMessageBox.ButtonRole.AcceptRole)
        box.setDefaultButton(ok_button)
        box.setEscapeButton(ok_button)
        license_button = box.addButton(
            self.tr("许可说明"), QMessageBox.ButtonRole.ActionRole
        )
        box.exec()
        if box.clickedButton() is license_button:
            self.on_licenses_clicked()
    
    def on_licenses_clicked(self):
        root = (
            Path(sys.executable).resolve().parent
            if getattr(sys, "frozen", False)
            else Path(__file__).resolve().parent.parent
        )
        files = [
            (self.tr("项目许可证（MIT）"), root / "LICENSE"),
           (self.tr("第三方组件与许可"), root / "THIRD_PARTY_NOTICES.md"),
        ]
        files += [
            (p.name, p)
            for p in sorted((root / "licenses").glob("*.txt"))
       ]
        dialog = QDialog(self)
        dialog.setWindowTitle(self.tr("许可说明"))
        dialog.resize(760, 520)
        selector = QComboBox(dialog)
        viewer = QTextBrowser(dialog)
        viewer.setReadOnly(True)
        viewer.setTabChangesFocus(True)
        viewer.setOpenLinks(False)
        close_button = QPushButton(self.tr("关闭"), dialog)
        close_button.clicked.connect(dialog.accept)
        for name, path in files:
            selector.addItem(name, str(path))
        def show_file(index):
            path = Path(selector.itemData(index))
            viewer.document().setBaseUrl(QUrl.fromLocalFile(str(path)))
            try:
                text = path.read_text(encoding="utf-8-sig")
            except (OSError, UnicodeError) as error:
                text = self.tr("无法读取文件：{path}\n{error}").format(
                    path=path, error=error
                )
                viewer.setPlainText(text)
                return
            if path.suffix.lower() in {".md", ".mkd", ".markdown"}:
                viewer.setMarkdown(text)
            else:
                viewer.setPlainText(text)

        def open_link(url):
            target = viewer.document().baseUrl().resolved(url)
            if target.isLocalFile():
                path = Path(target.toLocalFile()).resolve()
                for index in range(selector.count()):
                    if Path(selector.itemData(index)).resolve() == path:
                        selector.setCurrentIndex(index)
                        return
            QDesktopServices.openUrl(target)

        viewer.anchorClicked.connect(open_link)
        selector.currentIndexChanged.connect(show_file)
        show_file(0)
        layout = QVBoxLayout(dialog)
        layout.addWidget(selector)
        layout.addWidget(viewer, 1)
        layout.addWidget(close_button, 0, Qt.AlignmentFlag.AlignRight)
        dialog.finished.connect(dialog.deleteLater)
        dialog.open()
    

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = LsConvWindow()
    window.show()

    sys.exit(app.exec())
