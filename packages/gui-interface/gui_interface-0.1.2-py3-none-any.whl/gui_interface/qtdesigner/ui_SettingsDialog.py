# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QCommandLinkButton,
    QDial,
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QWidget,
)


class Ui_Settings(object):
    def setupUi(self, Settings):
        if not Settings.objectName():
            Settings.setObjectName("Settings")
        Settings.resize(596, 433)
        self.formLayout = QFormLayout(Settings)
        self.formLayout.setObjectName("formLayout")
        self.label_port = QLabel(Settings)
        self.label_port.setObjectName("label_port")
        font = QFont()
        font.setPointSize(11)
        self.label_port.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_port)

        self.lineEdit_port = QLineEdit(Settings)
        self.lineEdit_port.setObjectName("lineEdit_port")
        self.lineEdit_port.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit_port)

        self.label_serial = QLabel(Settings)
        self.label_serial.setObjectName("label_serial")
        self.label_serial.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_serial)

        self.lineEdit_serial = QLineEdit(Settings)
        self.lineEdit_serial.setObjectName("lineEdit_serial")
        self.lineEdit_serial.setFont(font)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.lineEdit_serial)

        self.label_chip = QLabel(Settings)
        self.label_chip.setObjectName("label_chip")
        self.label_chip.setFont(font)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_chip)

        self.comboBox_chip = QComboBox(Settings)
        self.comboBox_chip.setObjectName("comboBox_chip")
        self.comboBox_chip.setFont(font)
        self.comboBox_chip.setFrame(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.comboBox_chip)

        self.checkBox_connect = QCheckBox(Settings)
        self.checkBox_connect.setObjectName("checkBox_connect")
        self.checkBox_connect.setFont(font)

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.checkBox_connect)

        self.label_3 = QLabel(Settings)
        self.label_3.setObjectName("label_3")
        self.label_3.setFont(font)
        self.label_3.setMargin(4)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.label_3)

        self.checkBox_logon = QCheckBox(Settings)
        self.checkBox_logon.setObjectName("checkBox_logon")
        self.checkBox_logon.setFont(font)

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.checkBox_logon)

        self.spinBox_autologoff_delay = QSpinBox(Settings)
        self.spinBox_autologoff_delay.setObjectName("spinBox_autologoff_delay")
        self.spinBox_autologoff_delay.setFont(font)
        self.spinBox_autologoff_delay.setProperty("showGroupSeparator", False)
        self.spinBox_autologoff_delay.setMinimum(1)

        self.formLayout.setWidget(
            4, QFormLayout.FieldRole, self.spinBox_autologoff_delay
        )

        self.checkBox_debug = QCheckBox(Settings)
        self.checkBox_debug.setObjectName("checkBox_debug")
        self.checkBox_debug.setFont(font)

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.checkBox_debug)

        self.commandLinkButton_select_color = QCommandLinkButton(Settings)
        self.commandLinkButton_select_color.setObjectName(
            "commandLinkButton_select_color"
        )

        self.formLayout.setWidget(
            5, QFormLayout.FieldRole, self.commandLinkButton_select_color
        )

        self.checkBox_test = QCheckBox(Settings)
        self.checkBox_test.setObjectName("checkBox_test")
        self.checkBox_test.setFont(font)

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.checkBox_test)

        self.commandLinkButton_bg_color = QCommandLinkButton(Settings)
        self.commandLinkButton_bg_color.setObjectName("commandLinkButton_bg_color")
        font1 = QFont()
        font1.setFamilies(["Segoe UI"])
        font1.setPointSize(11)
        self.commandLinkButton_bg_color.setFont(font1)

        self.formLayout.setWidget(
            6, QFormLayout.FieldRole, self.commandLinkButton_bg_color
        )

        self.label_2 = QLabel(Settings)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.label_2)

        self.spinBox_arduino_id = QSpinBox(Settings)
        self.spinBox_arduino_id.setObjectName("spinBox_arduino_id")
        self.spinBox_arduino_id.setFont(font)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.spinBox_arduino_id)

        self.label = QLabel(Settings)
        self.label.setObjectName("label")
        self.label.setFont(font)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.label)

        self.pushButton_save = QPushButton(Settings)
        self.pushButton_save.setObjectName("pushButton_save")
        self.pushButton_save.setFont(font)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.pushButton_save)

        self.label_speed = QLabel(Settings)
        self.label_speed.setObjectName("label_speed")
        self.label_speed.setFont(font)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.label_speed)

        self.dial = QDial(Settings)
        self.dial.setObjectName("dial")
        self.dial.setFont(font)
        self.dial.setMinimum(10)
        self.dial.setMaximum(225)
        self.dial.setValue(50)
        self.dial.setOrientation(Qt.Horizontal)
        self.dial.setInvertedAppearance(True)
        self.dial.setInvertedControls(False)
        self.dial.setNotchesVisible(True)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.dial)

        self.retranslateUi(Settings)

        self.comboBox_chip.setCurrentIndex(-1)

        QMetaObject.connectSlotsByName(Settings)

    # setupUi

    def retranslateUi(self, Settings):
        Settings.setWindowTitle(QCoreApplication.translate("Settings", "Dialog", None))
        self.label_port.setText(
            QCoreApplication.translate("Settings", "SerialPort", None)
        )
        self.label_serial.setText(
            QCoreApplication.translate("Settings", "Pgmr Serial", None)
        )
        self.label_chip.setText(QCoreApplication.translate("Settings", "Chip", None))
        self.checkBox_connect.setText(
            QCoreApplication.translate("Settings", "Auto Connect", None)
        )
        self.label_3.setText(
            QCoreApplication.translate("Settings", "Auto Logoff Delay:", None)
        )
        self.checkBox_logon.setText(
            QCoreApplication.translate("Settings", "Auto Login", None)
        )
        self.spinBox_autologoff_delay.setSpecialValueText("")
        self.checkBox_debug.setText(
            QCoreApplication.translate("Settings", "Debug", None)
        )
        self.commandLinkButton_select_color.setText(
            QCoreApplication.translate("Settings", "Select Text Color", None)
        )
        self.checkBox_test.setText(
            QCoreApplication.translate("Settings", "Auto Test", None)
        )
        self.commandLinkButton_bg_color.setText(
            QCoreApplication.translate("Settings", "Select Background Color", None)
        )
        self.label_2.setText(QCoreApplication.translate("Settings", "Arduino ID", None))
        self.label.setText(QCoreApplication.translate("Settings", "Test Speed", None))
        self.pushButton_save.setText(
            QCoreApplication.translate("Settings", "Save", None)
        )
        self.label_speed.setText(
            QCoreApplication.translate("Settings", "TextLabel", None)
        )

    # retranslateUi
