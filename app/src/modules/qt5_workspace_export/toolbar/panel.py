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


class ToolbarWidget(QtWidgets.QScrollArea):
    actionExport = QtCore.pyqtSignal(object)
    actionPerformanceExport = QtCore.pyqtSignal(object)
    actionPowersave = QtCore.pyqtSignal(object)
    actionPowersaveExport = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, config=None):
        super(ToolbarWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidgetResizable(True)

        self.setContentsMargins(0, 0, 0, 0)

        from .button import ToolbarButton

        self.container = QtWidgets.QWidget()
        self.container.setLayout(QtWidgets.QHBoxLayout())
        self.container.layout().setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.setWidget(self.container)

        self.export = ToolbarButton(self, "Export rules", QtGui.QIcon('icons/export'))
        self.export.setToolTip('Export the current power configuration into the file')
        self.export.clicked.connect(self.actionExport.emit)
        self.addWidget(self.export)

        self.performanceExport = ToolbarButton(self, "Export performance", QtGui.QIcon('icons/performance'))
        self.performanceExport.setToolTip('Export the performance power configuration into the file')
        self.performanceExport.clicked.connect(self.actionPerformanceExport.emit)
        self.addWidget(self.performanceExport)

        self.powersaveExport = ToolbarButton(self, "Export powersave", QtGui.QIcon('icons/powersave'))
        self.powersaveExport.setToolTip('Export the powersave power configuration into the file')
        self.powersaveExport.clicked.connect(self.actionPowersaveExport.emit)
        self.addWidget(self.powersaveExport)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget)
