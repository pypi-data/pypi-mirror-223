# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddUserDialog.ui'
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
    QAbstractButton,
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
import resource_rc
import icons_rc


class Ui_AddUserDialog(object):
    def setupUi(self, AddUserDialog):
        if not AddUserDialog.objectName():
            AddUserDialog.setObjectName("AddUserDialog")
        AddUserDialog.resize(390, 160)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AddUserDialog.sizePolicy().hasHeightForWidth())
        AddUserDialog.setSizePolicy(sizePolicy)
        icon = QIcon()
        icon.addFile(
            ":/resources/icons/images/icons/follow.png",
            QSize(),
            QIcon.Normal,
            QIcon.Off,
        )
        AddUserDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(AddUserDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setVerticalSpacing(20)
        self.label = QLabel(AddUserDialog)
        self.label.setObjectName("label")
        font = QFont()
        font.setPointSize(11)
        self.label.setFont(font)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.lineEdit_username = QLineEdit(AddUserDialog)
        self.lineEdit_username.setObjectName("lineEdit_username")
        self.lineEdit_username.setFont(font)

        self.gridLayout.addWidget(self.lineEdit_username, 0, 1, 1, 1)

        self.label_2 = QLabel(AddUserDialog)
        self.label_2.setObjectName("label_2")
        self.label_2.setFont(font)

        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)

        self.lineEdit_password = QLineEdit(AddUserDialog)
        self.lineEdit_password.setObjectName("lineEdit_password")
        self.lineEdit_password.setFont(font)

        self.gridLayout.addWidget(self.lineEdit_password, 1, 1, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.checkBox = QCheckBox(AddUserDialog)
        self.checkBox.setObjectName("checkBox")
        self.checkBox.setFont(font)

        self.verticalLayout.addWidget(self.checkBox)

        self.buttonBox = QDialogButtonBox(AddUserDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(AddUserDialog)
        self.buttonBox.accepted.connect(AddUserDialog.accept)
        self.buttonBox.rejected.connect(AddUserDialog.reject)

        QMetaObject.connectSlotsByName(AddUserDialog)

    # setupUi

    def retranslateUi(self, AddUserDialog):
        AddUserDialog.setWindowTitle(
            QCoreApplication.translate("AddUserDialog", "Dialog", None)
        )
        self.label.setText(
            QCoreApplication.translate("AddUserDialog", "Username", None)
        )
        self.label_2.setText(
            QCoreApplication.translate("AddUserDialog", "Password", None)
        )
        self.checkBox.setText(
            QCoreApplication.translate("AddUserDialog", "Admin", None)
        )

    # retranslateUi
