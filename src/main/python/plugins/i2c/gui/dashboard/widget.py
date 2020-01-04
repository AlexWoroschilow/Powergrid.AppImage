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
import webbrowser

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .label import DashboardImage
from .label import DashboardTitle

from .button import DashboardButtonFlat
from .settings import DashboardSettings
from .properties import DashboardProperties
from .text import DashboardDescription


class DashboardWidget(QtWidgets.QFrame):
    theme = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(DashboardTitle('Inter-Integrated Circuit'), 0, 0, 1, 9)
        self.layout().addWidget(DashboardImage('icons/i2c'), 1, 0)
        self.layout().addWidget(DashboardSettings(), 1, 1, 1, 9)
        self.layout().addWidget(DashboardProperties(), 2, 0, 1, 10)
        self.layout().addWidget(DashboardDescription(), 3, 0, 1, 10)


    def linkClickedEvent(self, event):
        return webbrowser.open('https://www.kernel.org/doc/html/v4.12/driver-api/pm/devices.html')
