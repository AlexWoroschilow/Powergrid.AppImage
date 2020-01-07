# -*- coding: utf-8 -*-
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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .button import PictureButtonFlat


class Toolbar(QtWidgets.QFrame):
    schema_cleanup = QtCore.pyqtSignal(object)
    schema_apply = QtCore.pyqtSignal(object)

    def __init__(self):
        super(Toolbar, self).__init__()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.apply = PictureButtonFlat(QtGui.QIcon("icons/start"))
        self.apply.setText(' Apply current schema')
        self.apply.setShortcut("Ctrl+N")
        self.layout().addWidget(self.apply)

        self.cleanup = PictureButtonFlat(QtGui.QIcon("icons/cleanup"))
        self.cleanup.setText(' Remove schema from the system')
        self.cleanup.setShortcut("Ctrl+G")
        self.layout().addWidget(self.cleanup)

        self.cleanup.clicked.connect(self.schema_cleanup.emit)
        self.apply.clicked.connect(self.schema_apply.emit)

    def close(self):
        super(Toolbar, self).deleteLater()
        return super(Toolbar, self).close()
