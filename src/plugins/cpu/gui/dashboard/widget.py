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
import cpuinfo

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .label import DashboardTitle
from .statistic import DashboardImage
from .button import DashboardButtonFlat
from .settings import DashboardSettings
from .text import DashboardDescription
from .properties import DashboardProperties
from .schema import DashboardSchema


class DashboardWidget(QtWidgets.QFrame):

    def __init__(self):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(DashboardProperties(), 2, 0, 1, 10)
        self.layout().addWidget(DashboardSettings(), 3, 0, 1, 10)
        self.layout().addWidget(DashboardDescription(), 4, 0, 1, 10)
