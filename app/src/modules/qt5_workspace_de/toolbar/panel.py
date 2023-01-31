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
    actionGnome = QtCore.pyqtSignal(object)
    actionKDE = QtCore.pyqtSignal(object)
    actionXfce = QtCore.pyqtSignal(object)
    actionDeepin = QtCore.pyqtSignal(object)
    actionCinnamon = QtCore.pyqtSignal(object)
    actionBudgie = QtCore.pyqtSignal(object)

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

        self.kde = ToolbarButton(self, "KDE", QtGui.QIcon('icons/kde'))
        self.kde.setChecked(int(config.get('kde.enabled')))
        self.kde.clicked.connect(self.actionKDE.emit)
        self.addWidget(self.kde)

        self.gnome = ToolbarButton(self, "Gnome", QtGui.QIcon('icons/gnome'))
        self.gnome.setChecked(int(config.get('gnome.enabled')))
        self.gnome.clicked.connect(self.actionGnome.emit)
        self.addWidget(self.gnome)

        self.xfce = ToolbarButton(self, "Xfce", QtGui.QIcon('icons/xfce'))
        self.xfce.setChecked(int(config.get('xfce.enabled')))
        self.xfce.clicked.connect(self.actionXfce.emit)
        self.addWidget(self.xfce)

        self.deepin = ToolbarButton(self, "Deepin", QtGui.QIcon('icons/deepin'))
        self.deepin.setChecked(int(config.get('deepin.enabled')))
        self.deepin.clicked.connect(self.actionDeepin.emit)
        self.addWidget(self.deepin)

        self.cinnamon = ToolbarButton(self, "Cinnamon", QtGui.QIcon('icons/cinnamon'))
        self.cinnamon.setChecked(int(config.get('cinnamon.enabled')))
        self.cinnamon.clicked.connect(self.actionCinnamon.emit)
        self.addWidget(self.cinnamon)

        self.budgie = ToolbarButton(self, "Budgie", QtGui.QIcon('icons/budgie'))
        self.budgie.setChecked(int(config.get('budgie.enabled')))
        self.budgie.clicked.connect(self.actionBudgie.emit)
        self.addWidget(self.budgie)

    def addWidget(self, widget):
        self.container.layout().addWidget(widget)
