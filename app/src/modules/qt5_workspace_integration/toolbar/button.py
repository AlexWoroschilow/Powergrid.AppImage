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
import os
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ToolbarButton(QtWidgets.QToolButton):
    def __init__(self, parent=None, text=None, icon=None):
        super(ToolbarButton, self).__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.setIconSize(QtCore.QSize(20, 20))
        self.setIcon(QtGui.QIcon(icon))
        self.setFixedWidth(80)
        self.setCheckable(True)

        if text is not None and len(text):
            self.setToolTip(text)
            self.setText(text)


class ToolbarButtonIndicator(ToolbarButton):
    def __init__(self, parent=None, text=None, icon1=None, icon2=None):
        super(ToolbarButtonIndicator, self).__init__(parent, text, icon1)
        if not os.path.exists("/etc/udev/rules.d/70-performance.rules"): return self

        self.setIcon(QtGui.QIcon(icon2))


class PictureButtonDisabled(QtWidgets.QPushButton):

    def __init__(self, icon=None, parent=None):
        super(PictureButtonDisabled, self).__init__(icon, parent)
        self.setIconSize(QtCore.QSize(24, 24))
        self.setDisabled(False)
        self.setFlat(True)
        self.setIcon(icon)

    def event(self, QEvent):
        return super(QtWidgets.QPushButton, self).event(QEvent)
