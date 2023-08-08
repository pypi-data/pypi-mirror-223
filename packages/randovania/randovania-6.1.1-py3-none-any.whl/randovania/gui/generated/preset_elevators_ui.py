# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'preset_elevators.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

from randovania.gui.lib.scroll_protected import *  # type: ignore

class Ui_PresetElevators(object):
    def setupUi(self, PresetElevators):
        if not PresetElevators.objectName():
            PresetElevators.setObjectName(u"PresetElevators")
        PresetElevators.resize(505, 463)
        self.centralWidget = QWidget(PresetElevators)
        self.centralWidget.setObjectName(u"centralWidget")
        self.centralWidget.setMaximumSize(QSize(16777215, 16777215))
        self.elevator_parent_layout = QVBoxLayout(self.centralWidget)
        self.elevator_parent_layout.setSpacing(6)
        self.elevator_parent_layout.setContentsMargins(11, 11, 11, 11)
        self.elevator_parent_layout.setObjectName(u"elevator_parent_layout")
        self.elevator_parent_layout.setContentsMargins(0, 0, 0, 0)
        self.elevator_scroll_area = QScrollArea(self.centralWidget)
        self.elevator_scroll_area.setObjectName(u"elevator_scroll_area")
        self.elevator_scroll_area.setWidgetResizable(True)
        self.elevator_scroll_area_contents = QWidget()
        self.elevator_scroll_area_contents.setObjectName(u"elevator_scroll_area_contents")
        self.elevator_scroll_area_contents.setGeometry(QRect(0, 0, 503, 461))
        self.elevator_layout = QVBoxLayout(self.elevator_scroll_area_contents)
        self.elevator_layout.setSpacing(6)
        self.elevator_layout.setContentsMargins(11, 11, 11, 11)
        self.elevator_layout.setObjectName(u"elevator_layout")
        self.elevator_layout.setContentsMargins(4, 6, 4, 0)
        self.elevators_combo = ScrollProtectedComboBox(self.elevator_scroll_area_contents)
        self.elevators_combo.setObjectName(u"elevators_combo")

        self.elevator_layout.addWidget(self.elevators_combo)

        self.elevators_description_label = QLabel(self.elevator_scroll_area_contents)
        self.elevators_description_label.setObjectName(u"elevators_description_label")
        self.elevators_description_label.setScaledContents(True)
        self.elevators_description_label.setWordWrap(True)

        self.elevator_layout.addWidget(self.elevators_description_label)

        self.elevators_help_sound_bug_label = QLabel(self.elevator_scroll_area_contents)
        self.elevators_help_sound_bug_label.setObjectName(u"elevators_help_sound_bug_label")

        self.elevator_layout.addWidget(self.elevators_help_sound_bug_label)

        self.elevators_line_2 = QFrame(self.elevator_scroll_area_contents)
        self.elevators_line_2.setObjectName(u"elevators_line_2")
        self.elevators_line_2.setFrameShape(QFrame.HLine)
        self.elevators_line_2.setFrameShadow(QFrame.Sunken)

        self.elevator_layout.addWidget(self.elevators_line_2)

        self.skip_final_bosses_check = QCheckBox(self.elevator_scroll_area_contents)
        self.skip_final_bosses_check.setObjectName(u"skip_final_bosses_check")

        self.elevator_layout.addWidget(self.skip_final_bosses_check)

        self.skip_final_bosses_label = QLabel(self.elevator_scroll_area_contents)
        self.skip_final_bosses_label.setObjectName(u"skip_final_bosses_label")
        self.skip_final_bosses_label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.skip_final_bosses_label.setWordWrap(True)

        self.elevator_layout.addWidget(self.skip_final_bosses_label)

        self.elevators_line_4 = QFrame(self.elevator_scroll_area_contents)
        self.elevators_line_4.setObjectName(u"elevators_line_4")
        self.elevators_line_4.setFrameShape(QFrame.HLine)
        self.elevators_line_4.setFrameShadow(QFrame.Sunken)

        self.elevator_layout.addWidget(self.elevators_line_4)

        self.elevators_allow_unvisited_names_check = QCheckBox(self.elevator_scroll_area_contents)
        self.elevators_allow_unvisited_names_check.setObjectName(u"elevators_allow_unvisited_names_check")

        self.elevator_layout.addWidget(self.elevators_allow_unvisited_names_check)

        self.elevators_line_3 = QFrame(self.elevator_scroll_area_contents)
        self.elevators_line_3.setObjectName(u"elevators_line_3")
        self.elevators_line_3.setFrameShape(QFrame.HLine)
        self.elevators_line_3.setFrameShadow(QFrame.Sunken)

        self.elevator_layout.addWidget(self.elevators_line_3)

        self.elevators_help_list_label = QLabel(self.elevator_scroll_area_contents)
        self.elevators_help_list_label.setObjectName(u"elevators_help_list_label")
        self.elevators_help_list_label.setWordWrap(True)

        self.elevator_layout.addWidget(self.elevators_help_list_label)

        self.elevators_source_group = QGroupBox(self.elevator_scroll_area_contents)
        self.elevators_source_group.setObjectName(u"elevators_source_group")
        self.elevators_source_layout = QGridLayout(self.elevators_source_group)
        self.elevators_source_layout.setSpacing(3)
        self.elevators_source_layout.setContentsMargins(11, 11, 11, 11)
        self.elevators_source_layout.setObjectName(u"elevators_source_layout")
        self.elevators_source_layout.setContentsMargins(1, 1, 1, 1)

        self.elevator_layout.addWidget(self.elevators_source_group)

        self.elevators_target_group = QGroupBox(self.elevator_scroll_area_contents)
        self.elevators_target_group.setObjectName(u"elevators_target_group")
        self.elevators_target_layout = QGridLayout(self.elevators_target_group)
        self.elevators_target_layout.setSpacing(3)
        self.elevators_target_layout.setContentsMargins(11, 11, 11, 11)
        self.elevators_target_layout.setObjectName(u"elevators_target_layout")
        self.elevators_target_layout.setContentsMargins(1, 1, 1, 1)

        self.elevator_layout.addWidget(self.elevators_target_group)

        self.elevator_scroll_area.setWidget(self.elevator_scroll_area_contents)

        self.elevator_parent_layout.addWidget(self.elevator_scroll_area)

        PresetElevators.setCentralWidget(self.centralWidget)

        self.retranslateUi(PresetElevators)

        QMetaObject.connectSlotsByName(PresetElevators)
    # setupUi

    def retranslateUi(self, PresetElevators):
        PresetElevators.setWindowTitle(QCoreApplication.translate("PresetElevators", u"Elevators", None))
        self.elevators_description_label.setText(QCoreApplication.translate("PresetElevators", u"<html><head/><body><p>&lt;description generated dynamically&gt;</p></body></html>", None))
        self.elevators_help_sound_bug_label.setText(QCoreApplication.translate("PresetElevators", u"These settings will cause the elevator cutscenes to be silent in order to avoid a different game bug.", None))
        self.skip_final_bosses_check.setText(QCoreApplication.translate("PresetElevators", u"Go directly to credits from Sky Temple Gateway", None))
        self.skip_final_bosses_label.setText(QCoreApplication.translate("PresetElevators", u"<html><head/><body><p>Change the light beam in Sky Temple Gateway to go directly to the credits, skipping the final bosses.</p><p>This changes the requirements to <span style=\" font-weight:600;\">not need the final bosses</span>, turning certain items optional such as Screw Attack and Spider Ball.</p></body></html>", None))
        self.elevators_allow_unvisited_names_check.setText(QCoreApplication.translate("PresetElevators", u"Allow \"Always display room names on map\" when elevators are shuffled", None))
        self.elevators_help_list_label.setText(QCoreApplication.translate("PresetElevators", u"<html><head/><body><p>Shuffling Sky Temple Gateway, Sky Temple Energy Controller, Aerie and Aerie Transport Station is possible, but they're not included by default as they behave somewhat differently to other elevators.</p><p>The elevator in Aerie Transport Station is only available after you defeat Dark Samus 2.</p><p>When shuffling Sky Temple Energy Controller, you <span style=\" font-weight:600;\">must</span> enter Sky Temple Gateway via an elevator otherwise the game will crash.</p><p><span style=\" font-style:italic;\">Warning</span>: Entering Sky Temple Energy Controller from elsewhere causes the game to be stuck in a black screen in unknown conditions. The game is still running, so you can blindly use the menu mod to work around this issue.</p></body></html>", None))
        self.elevators_source_group.setTitle(QCoreApplication.translate("PresetElevators", u"Elevators to randomize", None))
        self.elevators_target_group.setTitle(QCoreApplication.translate("PresetElevators", u"Valid elevator targets", None))
    # retranslateUi

