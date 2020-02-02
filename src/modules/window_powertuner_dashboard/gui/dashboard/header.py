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
import inject

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .label import DashboardTitle
from .button import PictureButtonFlat


class DashboardHeader(QtWidgets.QWidget):
    settingsAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardHeader, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        title = DashboardTitle("{} {}".format("Performance tuner", "" \
            if not os.path.exists('/etc/performance-tuner') else u"\u2611"))

        button = PictureButtonFlat("icons/icons")
        button.clicked.connect(self.settingsAction.emit)

        self.layout().addWidget(title, 0, 0, 1, 9)
        self.layout().addWidget(button, 0, 10, 1, 1)
