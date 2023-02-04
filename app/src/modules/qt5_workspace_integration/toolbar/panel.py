# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import hexdi
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .button import ToolbarButton
from .indicator import ToolbarButtonIndicator
from .button import PictureButtonDisabled


class ToolbarWidget(QtWidgets.QScrollArea):
    actionApply = QtCore.pyqtSignal(object)
    actionPerformance = QtCore.pyqtSignal(object)
    actionPowersave = QtCore.pyqtSignal(object)
    actionCleanup = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidgetResizable(True)

        self.setContentsMargins(0, 0, 0, 0)

        self.container = QtWidgets.QWidget()
        self.container.setLayout(QtWidgets.QHBoxLayout())
        self.container.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidget(self.container)

        self.indicator = ToolbarButtonIndicator('icons/enabled-red.svg', 'icons/enabled-green.svg')
        self.addWidget(self.indicator)

        self.addWidget(PictureButtonDisabled(QtGui.QIcon("icons/folder")))

        self.apply = ToolbarButton(self, "Apply", QtGui.QIcon('icons/start'))
        self.apply.setToolTip("Apply the current power configuration")
        self.apply.clicked.connect(self.actionApply.emit)
        self.apply.setCheckable(False)
        self.addWidget(self.apply)

        self.apply_performance = ToolbarButton(self, "Performance", QtGui.QIcon('icons/performance'))
        self.apply_performance.setToolTip("Apply the performance power configuration")
        self.apply_performance.clicked.connect(self.actionPerformance.emit)
        self.apply_performance.setCheckable(False)
        self.addWidget(self.apply_performance)

        self.apply_powersave = ToolbarButton(self, "Powersave", QtGui.QIcon('icons/powersave'))
        self.apply_powersave.setToolTip("Apply the powersave power configuration")
        self.apply_powersave.clicked.connect(self.actionPowersave.emit)
        self.apply_powersave.setCheckable(False)
        self.addWidget(self.apply_powersave)

        self.cleanup = ToolbarButton(self, "Cleanup", QtGui.QIcon('icons/cleanup'))
        self.cleanup.setToolTip("Rollback the integration with the system")
        self.cleanup.clicked.connect(self.actionCleanup.emit)
        self.apply.setCheckable(False)
        self.addWidget(self.cleanup)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget)
