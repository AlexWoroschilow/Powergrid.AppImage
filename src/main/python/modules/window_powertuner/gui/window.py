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
import inject

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

from .content import WindowContent
from .bar import Toolbar


class MainWindow(QtWidgets.QMainWindow):
    schema_cleanup = QtCore.pyqtSignal(object)
    schema_apply = QtCore.pyqtSignal(object)

    resize_event = QtCore.pyqtSignal(object)
    exit = QtCore.pyqtSignal(object)

    @inject.params(themes='themes')
    def __init__(self, themes=None):
        super(MainWindow, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('AOD - Performance Tuner')
        self.setWindowIcon(QtGui.QIcon("icons/tuner"))

        self.setStyleSheet(themes.get_stylesheet())

        self.toolbar = Toolbar()
        self.toolbar.schema_cleanup.connect(self.schema_cleanup.emit)
        self.toolbar.schema_apply.connect(self.schema_apply.emit)

        self.content = WindowContent(self)
        self.setCentralWidget(self.content)

    def resizeEvent(self, event):
        self.resize_event.emit(event)

    @inject.params(container='container.dashboard')
    def show(self, container=None):
        self.content.layout().addWidget(container.widget)

        self.content.layout().addWidget(self.toolbar)

        super(MainWindow, self).show()
