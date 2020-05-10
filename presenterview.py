# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'presenterview.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(1216, 808)
        Form.setStyleSheet(u"#Form,\n"
"#thumbnailAreaWidget,\n"
"#bottomArea QLabel,\n"
"#imageArea,\n"
"#imageLabel\n"
"{\n"
" background-color: black;\n"
" color: white;\n"
"}")
        self.verticalLayout = QVBoxLayout(Form)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.imageArea = QScrollArea(Form)
        self.imageArea.setObjectName(u"imageArea")
        self.imageArea.setFocusPolicy(Qt.NoFocus)
        self.imageArea.setFrameShape(QFrame.NoFrame)
        self.imageArea.setLineWidth(0)
        self.imageArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.imageArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.imageArea.setWidgetResizable(False)
        self.imageArea.setAlignment(Qt.AlignCenter)
        self.imageLabel = QLabel()
        self.imageLabel.setObjectName(u"imageLabel")
        self.imageLabel.setGeometry(QRect(508, 311, 200, 25))
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.imageLabel.sizePolicy().hasHeightForWidth())
        self.imageLabel.setSizePolicy(sizePolicy)
        self.imageLabel.setScaledContents(False)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.imageLabel.setTextInteractionFlags(Qt.NoTextInteraction)
        self.imageArea.setWidget(self.imageLabel)

        self.verticalLayout.addWidget(self.imageArea)

        self.bottomArea = QWidget(Form)
        self.bottomArea.setObjectName(u"bottomArea")
        sizePolicy1 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.bottomArea.sizePolicy().hasHeightForWidth())
        self.bottomArea.setSizePolicy(sizePolicy1)
        self.bottomArea.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout_2 = QHBoxLayout(self.bottomArea)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.wallClock = QLabel(self.bottomArea)
        self.wallClock.setObjectName(u"wallClock")
        sizePolicy2 = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.wallClock.sizePolicy().hasHeightForWidth())
        self.wallClock.setSizePolicy(sizePolicy2)
        font = QFont()
        font.setPointSize(25)
        self.wallClock.setFont(font)
        self.wallClock.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.wallClock)

        self.thumbnailArea = QScrollArea(self.bottomArea)
        self.thumbnailArea.setObjectName(u"thumbnailArea")
        self.thumbnailArea.setMaximumSize(QSize(16777215, 16777215))
        self.thumbnailArea.setFocusPolicy(Qt.NoFocus)
        self.thumbnailArea.setFrameShape(QFrame.NoFrame)
        self.thumbnailArea.setLineWidth(0)
        self.thumbnailArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.thumbnailArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.thumbnailArea.setWidgetResizable(True)
        self.thumbnailAreaWidget = QWidget()
        self.thumbnailAreaWidget.setObjectName(u"thumbnailAreaWidget")
        self.thumbnailAreaWidget.setGeometry(QRect(0, 0, 829, 162))
        self.gridLayout = QGridLayout(self.thumbnailAreaWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setVerticalSpacing(0)
        self.nextThumbnail = QLabel(self.thumbnailAreaWidget)
        self.nextThumbnail.setObjectName(u"nextThumbnail")
        self.nextThumbnail.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.nextThumbnail, 0, 2, 1, 1)

        self.currentThumbnail = QLabel(self.thumbnailAreaWidget)
        self.currentThumbnail.setObjectName(u"currentThumbnail")
        sizePolicy.setHeightForWidth(self.currentThumbnail.sizePolicy().hasHeightForWidth())
        self.currentThumbnail.setSizePolicy(sizePolicy)
        self.currentThumbnail.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.currentThumbnail, 0, 1, 1, 1)

        self.previousThumbnail = QLabel(self.thumbnailAreaWidget)
        self.previousThumbnail.setObjectName(u"previousThumbnail")
        self.previousThumbnail.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.gridLayout.addWidget(self.previousThumbnail, 0, 0, 1, 1)

        self.thumbnailArea.setWidget(self.thumbnailAreaWidget)

        self.horizontalLayout_2.addWidget(self.thumbnailArea)

        self.presentationClock = QLabel(self.bottomArea)
        self.presentationClock.setObjectName(u"presentationClock")
        sizePolicy2.setHeightForWidth(self.presentationClock.sizePolicy().hasHeightForWidth())
        self.presentationClock.setSizePolicy(sizePolicy2)
        self.presentationClock.setFont(font)
        self.presentationClock.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.presentationClock)

        self.slideClock = QLabel(self.bottomArea)
        self.slideClock.setObjectName(u"slideClock")
        sizePolicy2.setHeightForWidth(self.slideClock.sizePolicy().hasHeightForWidth())
        self.slideClock.setSizePolicy(sizePolicy2)
        font1 = QFont()
        font1.setPointSize(50)
        self.slideClock.setFont(font1)
        self.slideClock.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_2.addWidget(self.slideClock)

        self.thumbnailArea.raise_()
        self.presentationClock.raise_()
        self.wallClock.raise_()
        self.slideClock.raise_()

        self.verticalLayout.addWidget(self.bottomArea)

        self.verticalLayout.setStretch(0, 80)
        self.verticalLayout.setStretch(1, 20)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"DS PDF Viewer", None))
        self.imageLabel.setText(QCoreApplication.translate("Form", u"The actual image goes here.", None))
        self.wallClock.setText(QCoreApplication.translate("Form", u"09:12:34", None))
        self.nextThumbnail.setText(QCoreApplication.translate("Form", u"Next Page", None))
        self.currentThumbnail.setText(QCoreApplication.translate("Form", u"Current Page", None))
        self.previousThumbnail.setText(QCoreApplication.translate("Form", u"Previous Page", None))
        self.presentationClock.setText(QCoreApplication.translate("Form", u"Total\n"
"00:00:00", None))
        self.slideClock.setText(QCoreApplication.translate("Form", u"00:00", None))
    # retranslateUi

