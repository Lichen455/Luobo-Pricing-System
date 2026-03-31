# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QApplication, QComboBox, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

class Ui_Widget(object):
    def setupUi(self, Widget):
        if not Widget.objectName():
            Widget.setObjectName(u"Widget")
        Widget.resize(912, 621)
        self.scrollArea = QScrollArea(Widget)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setGeometry(QRect(190, 40, 691, 521))
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scrollArea.sizePolicy().hasHeightForWidth())
        self.scrollArea.setSizePolicy(sizePolicy)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 689, 519))
        self.verticalLayout = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.comboBox = QComboBox(Widget)
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(190, 10, 171, 25))
        self.pushButton_update = QPushButton(Widget)
        self.pushButton_update.setObjectName(u"pushButton_update")
        self.pushButton_update.setGeometry(QRect(730, 570, 151, 41))
        self.pushButton_input = QPushButton(Widget)
        self.pushButton_input.setObjectName(u"pushButton_input")
        self.pushButton_input.setGeometry(QRect(20, 20, 93, 28))
        self.comboBox_2 = QComboBox(Widget)
        self.comboBox_2.setObjectName(u"comboBox_2")
        self.comboBox_2.setGeometry(QRect(710, 10, 171, 25))
        self.pushButton_fill = QPushButton(Widget)
        self.pushButton_fill.setObjectName(u"pushButton_fill")
        self.pushButton_fill.setGeometry(QRect(20, 70, 93, 28))
        self.pushButton_compute = QPushButton(Widget)
        self.pushButton_compute.setObjectName(u"pushButton_compute")
        self.pushButton_compute.setGeometry(QRect(20, 120, 93, 28))
        self.pushButton_all = QPushButton(Widget)
        self.pushButton_all.setObjectName(u"pushButton_all")
        self.pushButton_all.setGeometry(QRect(20, 170, 131, 31))
        self.pushButton_all.setStyleSheet(u"")
        self.comboBox_3 = QComboBox(Widget)
        self.comboBox_3.setObjectName(u"comboBox_3")
        self.comboBox_3.setGeometry(QRect(382, 10, 121, 25))
        self.label = QLabel(Widget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(365, 10, 16, 20))

        self.retranslateUi(Widget)

        QMetaObject.connectSlotsByName(Widget)
    # setupUi

    def retranslateUi(self, Widget):
        Widget.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.pushButton_update.setText(QCoreApplication.translate("Widget", u"\u66f4\u65b0\u4ef7\u683c\u8868\u4e0e\u5dee\u4ef7\u8868", None))
        self.pushButton_input.setText(QCoreApplication.translate("Widget", u"\u5bfc\u5165\u6570\u636e", None))
        self.pushButton_fill.setText(QCoreApplication.translate("Widget", u"\u586b\u5145\u6570\u636e", None))
        self.pushButton_compute.setText(QCoreApplication.translate("Widget", u"\u8ba1\u7b97\u6570\u636e", None))
        self.pushButton_all.setText(QCoreApplication.translate("Widget", u"\u4e00\u952e\u586b\u5145/\u8ba1\u7b97", None))
        self.label.setText(QCoreApplication.translate("Widget", u"+", None))
    # retranslateUi

