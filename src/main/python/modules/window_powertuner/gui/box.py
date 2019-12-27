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
import os
import hexdi

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from PyQt5.QtCore import Qt

from .content import WindowContent
from .bar import Toolbar


class MessageBox(QtWidgets.QMessageBox):

    @hexdi.inject('themes')
    def __init__(self, parent=None, themes=None):
        super(MessageBox, self).__init__(parent)
        self.setContentsMargins(0, 0, 0, 0)
        self.setWindowTitle('AOD - Power Tuner')
        self.setWindowIcon(QtGui.QIcon("icons/tuner"))
        self.setStyleSheet(themes.get_stylesheet())
