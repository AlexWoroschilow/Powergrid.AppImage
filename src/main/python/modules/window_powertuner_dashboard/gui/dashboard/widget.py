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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .label import DashboardTitle
from .statistic import DashboardImage
from .text import DashboardDescription
from .text import DashboardDescriptionDeviceManagement
from .text import DashboardDescriptionACAdapter
from .text import DashboardDescriptionBattery

from .settings import DashboardSettingsPerformance
from .settings import DashboardSettingsPowersave
from .settings import DashboardSettingsDevices


class DashboardWidget(QtWidgets.QWidget):

    def __init__(self):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(DashboardTitle("Performance tuner"))
        self.layout().addWidget(DashboardDescription())
        self.layout().addWidget(DashboardImage())

        self.layout().addWidget(DashboardTitle("AC- Adapter"))
        self.layout().addWidget(DashboardDescriptionACAdapter())
        self.layout().addWidget(DashboardSettingsPerformance())

        self.layout().addWidget(DashboardTitle("Battery"))
        self.layout().addWidget(DashboardDescriptionBattery())
        self.layout().addWidget(DashboardSettingsPowersave())

        self.layout().addWidget(DashboardTitle("Device management"))
        self.layout().addWidget(DashboardDescriptionDeviceManagement())
        self.layout().addWidget(DashboardSettingsDevices())
