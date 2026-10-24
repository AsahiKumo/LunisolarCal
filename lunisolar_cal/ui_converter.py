# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'lsconv.ui'
##
## Created by: Qt User Interface Compiler version 6.11.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QVBoxLayout,
    QWidget)
from . import resources_rc

class Ui_LsConvWindow(object):
    def setupUi(self, LsConvWindow):
        if not LsConvWindow.objectName():
            LsConvWindow.setObjectName(u"LsConvWindow")
        LsConvWindow.resize(481, 361)
        icon = QIcon()
        icon.addFile(u":/icons/calendar.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        LsConvWindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(LsConvWindow)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(16, 16, 16, 16)
        self.ttlLabel = QLabel(LsConvWindow)
        self.ttlLabel.setObjectName(u"ttlLabel")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ttlLabel.sizePolicy().hasHeightForWidth())
        self.ttlLabel.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.ttlLabel)

        self.langRow = QWidget(LsConvWindow)
        self.langRow.setObjectName(u"langRow")
        sizePolicy.setHeightForWidth(self.langRow.sizePolicy().hasHeightForWidth())
        self.langRow.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.langRow)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.langLabel = QLabel(self.langRow)
        self.langLabel.setObjectName(u"langLabel")

        self.horizontalLayout_3.addWidget(self.langLabel)

        self.langCombo = QComboBox(self.langRow)
        self.langCombo.addItem("")
        self.langCombo.addItem("")
        self.langCombo.addItem("")
        self.langCombo.setObjectName(u"langCombo")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.langCombo.sizePolicy().hasHeightForWidth())
        self.langCombo.setSizePolicy(sizePolicy1)
        self.langCombo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)

        self.horizontalLayout_3.addWidget(self.langCombo)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)

        self.aboutButton = QPushButton(self.langRow)
        self.aboutButton.setObjectName(u"aboutButton")
        sizePolicy1.setHeightForWidth(self.aboutButton.sizePolicy().hasHeightForWidth())
        self.aboutButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.aboutButton)


        self.verticalLayout.addWidget(self.langRow)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.calLabel = QLabel(LsConvWindow)
        self.calLabel.setObjectName(u"calLabel")

        self.horizontalLayout.addWidget(self.calLabel)

        self.calCombo = QComboBox(LsConvWindow)
        self.calCombo.addItem("")
        self.calCombo.addItem("")
        self.calCombo.setObjectName(u"calCombo")
        sizePolicy1.setHeightForWidth(self.calCombo.sizePolicy().hasHeightForWidth())
        self.calCombo.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.calCombo)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_4)

        self.chineseCheck = QCheckBox(LsConvWindow)
        self.chineseCheck.setObjectName(u"chineseCheck")
        sizePolicy1.setHeightForWidth(self.chineseCheck.sizePolicy().hasHeightForWidth())
        self.chineseCheck.setSizePolicy(sizePolicy1)
        self.chineseCheck.setChecked(True)

        self.horizontalLayout.addWidget(self.chineseCheck)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.todayButton = QPushButton(LsConvWindow)
        self.todayButton.setObjectName(u"todayButton")
        sizePolicy1.setHeightForWidth(self.todayButton.sizePolicy().hasHeightForWidth())
        self.todayButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.todayButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(12)
        self.gridLayout.setVerticalSpacing(8)
        self.yearLabel = QLabel(LsConvWindow)
        self.yearLabel.setObjectName(u"yearLabel")
        sizePolicy.setHeightForWidth(self.yearLabel.sizePolicy().hasHeightForWidth())
        self.yearLabel.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.yearLabel, 0, 0, 1, 1)

        self.monthLabel = QLabel(LsConvWindow)
        self.monthLabel.setObjectName(u"monthLabel")
        sizePolicy.setHeightForWidth(self.monthLabel.sizePolicy().hasHeightForWidth())
        self.monthLabel.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.monthLabel, 0, 1, 1, 1)

        self.dayLabel = QLabel(LsConvWindow)
        self.dayLabel.setObjectName(u"dayLabel")
        sizePolicy.setHeightForWidth(self.dayLabel.sizePolicy().hasHeightForWidth())
        self.dayLabel.setSizePolicy(sizePolicy)

        self.gridLayout.addWidget(self.dayLabel, 0, 2, 1, 1)

        self.yearSpin = QSpinBox(LsConvWindow)
        self.yearSpin.setObjectName(u"yearSpin")
        self.yearSpin.setMinimum(1)
        self.yearSpin.setMaximum(9999)
        self.yearSpin.setValue(2024)

        self.gridLayout.addWidget(self.yearSpin, 1, 0, 1, 1)

        self.monthSpin = QSpinBox(LsConvWindow)
        self.monthSpin.setObjectName(u"monthSpin")
        self.monthSpin.setMinimum(1)
        self.monthSpin.setMaximum(12)
        self.monthSpin.setValue(2)

        self.gridLayout.addWidget(self.monthSpin, 1, 1, 1, 1)

        self.daySpin = QSpinBox(LsConvWindow)
        self.daySpin.setObjectName(u"daySpin")
        self.daySpin.setMinimum(1)
        self.daySpin.setMaximum(31)
        self.daySpin.setValue(10)

        self.gridLayout.addWidget(self.daySpin, 1, 2, 1, 1)

        self.leapCheck = QCheckBox(LsConvWindow)
        self.leapCheck.setObjectName(u"leapCheck")
        self.leapCheck.setChecked(False)

        self.gridLayout.addWidget(self.leapCheck, 2, 1, 1, 1)


        self.verticalLayout.addLayout(self.gridLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_3 = QSpacerItem(148, 28, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_3)

        self.convButton = QPushButton(LsConvWindow)
        self.convButton.setObjectName(u"convButton")
        sizePolicy1.setHeightForWidth(self.convButton.sizePolicy().hasHeightForWidth())
        self.convButton.setSizePolicy(sizePolicy1)
        icon1 = QIcon()
        icon1.addFile(u":/icons/convert.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.convButton.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.convButton)

        self.copyButton = QPushButton(LsConvWindow)
        self.copyButton.setObjectName(u"copyButton")
        self.copyButton.setEnabled(False)
        sizePolicy1.setHeightForWidth(self.copyButton.sizePolicy().hasHeightForWidth())
        self.copyButton.setSizePolicy(sizePolicy1)

        self.horizontalLayout_2.addWidget(self.copyButton)

        self.horizontalSpacer_2 = QSpacerItem(148, 28, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(3, 1)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.resultLabel = QLabel(LsConvWindow)
        self.resultLabel.setObjectName(u"resultLabel")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.resultLabel.sizePolicy().hasHeightForWidth())
        self.resultLabel.setSizePolicy(sizePolicy2)
        self.resultLabel.setFrameShape(QFrame.Shape.Box)
        self.resultLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.resultLabel.setWordWrap(True)
        self.resultLabel.setMargin(10)
        self.resultLabel.setTextInteractionFlags(Qt.TextInteractionFlag.LinksAccessibleByMouse|Qt.TextInteractionFlag.TextSelectableByMouse)

        self.verticalLayout.addWidget(self.resultLabel)

        self.verticalLayout.setStretch(5, 1)
        QWidget.setTabOrder(self.langCombo, self.calCombo)
        QWidget.setTabOrder(self.calCombo, self.yearSpin)
        QWidget.setTabOrder(self.yearSpin, self.monthSpin)
        QWidget.setTabOrder(self.monthSpin, self.daySpin)
        QWidget.setTabOrder(self.daySpin, self.leapCheck)
        QWidget.setTabOrder(self.leapCheck, self.chineseCheck)
        QWidget.setTabOrder(self.chineseCheck, self.todayButton)
        QWidget.setTabOrder(self.todayButton, self.convButton)
        QWidget.setTabOrder(self.convButton, self.copyButton)

        self.retranslateUi(LsConvWindow)

        self.langCombo.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(LsConvWindow)
    # setupUi

    def retranslateUi(self, LsConvWindow):
        LsConvWindow.setWindowTitle(QCoreApplication.translate("LsConvWindow", u"\u516c\u519c\u5386\u8f6c\u6362", None))
        self.ttlLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u8bf7\u8f93\u5165\u9700\u8981\u8f6c\u6362\u7684\u65e5\u671f\uff1a", None))
        self.langLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u754c\u9762\u8bed\u8a00\uff1a", None))
        self.langCombo.setItemText(0, QCoreApplication.translate("LsConvWindow", u"\u7b80\u4f53\u4e2d\u6587", None))
        self.langCombo.setItemText(1, QCoreApplication.translate("LsConvWindow", u"English", None))
        self.langCombo.setItemText(2, QCoreApplication.translate("LsConvWindow", u"\u8ddf\u968f\u7cfb\u7edf", None))

        self.aboutButton.setText(QCoreApplication.translate("LsConvWindow", u"\u5173\u4e8e", None))
        self.calLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u8f93\u5165\u5386\u6cd5\uff1a", None))
        self.calCombo.setItemText(0, QCoreApplication.translate("LsConvWindow", u"\u516c\u5386", None))
        self.calCombo.setItemText(1, QCoreApplication.translate("LsConvWindow", u"\u519c\u5386", None))

        self.chineseCheck.setText(QCoreApplication.translate("LsConvWindow", u"\u4e2d\u6587\u519c\u5386\u8868\u793a", None))
        self.todayButton.setText(QCoreApplication.translate("LsConvWindow", u"\u4eca\u5929", None))
        self.yearLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u5e74\u4efd\uff1a", None))
        self.monthLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u6708\u4efd\uff1a", None))
        self.dayLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u65e5\u671f\uff1a", None))
        self.leapCheck.setText(QCoreApplication.translate("LsConvWindow", u"\u95f0\u6708\uff08\u519c\u5386\uff09", None))
        self.convButton.setText(QCoreApplication.translate("LsConvWindow", u"\u8f6c\u6362", None))
        self.copyButton.setText(QCoreApplication.translate("LsConvWindow", u"\u590d\u5236\u7ed3\u679c", None))
        self.resultLabel.setText(QCoreApplication.translate("LsConvWindow", u"\u7b49\u5f85\u8f6c\u6362", None))
    # retranslateUi

