# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'am2r_game_export_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

class Ui_AM2RGameExportDialog(object):
    def setupUi(self, AM2RGameExportDialog):
        if not AM2RGameExportDialog.objectName():
            AM2RGameExportDialog.setObjectName(u"AM2RGameExportDialog")
        AM2RGameExportDialog.resize(508, 270)
        self.gridLayout = QGridLayout(AM2RGameExportDialog)
        self.gridLayout.setSpacing(6)
        self.gridLayout.setContentsMargins(11, 11, 11, 11)
        self.gridLayout.setObjectName(u"gridLayout")
        self.input_file_edit = QLineEdit(AM2RGameExportDialog)
        self.input_file_edit.setObjectName(u"input_file_edit")

        self.gridLayout.addWidget(self.input_file_edit, 2, 0, 1, 1)

        self.line = QFrame(AM2RGameExportDialog)
        self.line.setObjectName(u"line")
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.gridLayout.addWidget(self.line, 5, 0, 1, 2)

        self.input_file_button = QPushButton(AM2RGameExportDialog)
        self.input_file_button.setObjectName(u"input_file_button")

        self.gridLayout.addWidget(self.input_file_button, 2, 1, 1, 1)

        self.cancel_button = QPushButton(AM2RGameExportDialog)
        self.cancel_button.setObjectName(u"cancel_button")

        self.gridLayout.addWidget(self.cancel_button, 11, 1, 1, 1)

        self.description_label = QLabel(AM2RGameExportDialog)
        self.description_label.setObjectName(u"description_label")
        self.description_label.setWordWrap(True)

        self.gridLayout.addWidget(self.description_label, 0, 0, 1, 2)

        self.output_file_edit = QLineEdit(AM2RGameExportDialog)
        self.output_file_edit.setObjectName(u"output_file_edit")

        self.gridLayout.addWidget(self.output_file_edit, 4, 0, 1, 1)

        self.output_file_label = QLabel(AM2RGameExportDialog)
        self.output_file_label.setObjectName(u"output_file_label")

        self.gridLayout.addWidget(self.output_file_label, 3, 0, 1, 1)

        self.output_file_button = QPushButton(AM2RGameExportDialog)
        self.output_file_button.setObjectName(u"output_file_button")

        self.gridLayout.addWidget(self.output_file_button, 4, 1, 1, 1)

        self.output_format_label = QLabel(AM2RGameExportDialog)
        self.output_format_label.setObjectName(u"output_format_label")

        self.gridLayout.addWidget(self.output_format_label, 6, 0, 1, 1)

        self.input_file_label = QLabel(AM2RGameExportDialog)
        self.input_file_label.setObjectName(u"input_file_label")

        self.gridLayout.addWidget(self.input_file_label, 1, 0, 1, 1)

        self.auto_save_spoiler_check = QCheckBox(AM2RGameExportDialog)
        self.auto_save_spoiler_check.setObjectName(u"auto_save_spoiler_check")

        self.gridLayout.addWidget(self.auto_save_spoiler_check, 7, 0, 1, 1)

        self.accept_button = QPushButton(AM2RGameExportDialog)
        self.accept_button.setObjectName(u"accept_button")

        self.gridLayout.addWidget(self.accept_button, 11, 0, 1, 1)


        self.retranslateUi(AM2RGameExportDialog)

        QMetaObject.connectSlotsByName(AM2RGameExportDialog)
    # setupUi

    def retranslateUi(self, AM2RGameExportDialog):
        AM2RGameExportDialog.setWindowTitle(QCoreApplication.translate("AM2RGameExportDialog", u"Game Patching", None))
        self.input_file_edit.setPlaceholderText(QCoreApplication.translate("AM2RGameExportDialog", u"Path to AM2R 1.5.5 folder", None))
        self.input_file_button.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Select Folder", None))
        self.cancel_button.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Cancel", None))
        self.description_label.setText(QCoreApplication.translate("AM2RGameExportDialog", u"<html><head/><body><p>In order to create the randomized game, a 1.5.5 folder for AM2R is necessary.</p></body></html>", None))
        self.output_file_edit.setPlaceholderText(QCoreApplication.translate("AM2RGameExportDialog", u"Path where to place the randomized game", None))
        self.output_file_label.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Output Directory", None))
        self.output_file_button.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Select Folder", None))
        self.output_format_label.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Output Format", None))
        self.input_file_label.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Input Directory (1.5.5)", None))
        self.auto_save_spoiler_check.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Include a spoiler log on same directory", None))
        self.accept_button.setText(QCoreApplication.translate("AM2RGameExportDialog", u"Accept", None))
    # retranslateUi

