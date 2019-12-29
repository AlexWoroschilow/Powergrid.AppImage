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

from .label import DashboardImage
from .label import DashboardTitle

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
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(DashboardTitle(self.title), 0, 0, 1, 9)
        self.layout().addWidget(DashboardImage('icons/cpu'), 1, 0)
        self.layout().addWidget(DashboardSettings(), 1, 1, 1, 9)
        self.layout().addWidget(DashboardSchema(), 2, 0, 1, 10)
        self.layout().addWidget(DashboardDescription(), 3, 0, 1, 10)
        self.layout().addWidget(DashboardProperties(), 4, 0, 1, 10)

        self.link = DashboardButtonFlat("icons/linux", ' kernel.org')
        self.link.clicked.connect(self.linkClickedEvent)

        self.layout().addWidget(self.link, 0, 9)

    @property
    def title(self):
        cpu = cpuinfo.get_cpu_info()
        if len(cpu) and 'brand' in cpu:
            return cpu['brand']
        return "Unknown CPU"

    def linkClickedEvent(self, event):
        return webbrowser.open('https://www.kernel.org/doc/html/v4.16/admin-guide/pm/cpufreq.html')
