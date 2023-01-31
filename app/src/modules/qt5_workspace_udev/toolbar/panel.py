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


class ToolbarWidget(QtWidgets.QScrollArea):
    actionApply = QtCore.pyqtSignal(object)
    actionPerformance = QtCore.pyqtSignal(object)
    actionPowersave = QtCore.pyqtSignal(object)
    actionExport = QtCore.pyqtSignal(object)
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

        self.apply = ToolbarButton(self, "Apply schema", QtGui.QIcon('icons/start'))
        self.apply.clicked.connect(self.actionApply.emit)
        self.addWidget(self.apply)

        self.export = ToolbarButton(self, "Export to file", QtGui.QIcon('icons/export'))
        self.export.clicked.connect(self.actionExport.emit)
        self.addWidget(self.export)

        self.cleanup = ToolbarButton(self, "Cleanup", QtGui.QIcon('icons/cleanup'))
        self.cleanup.clicked.connect(self.actionCleanup.emit)
        self.addWidget(self.cleanup)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget)
