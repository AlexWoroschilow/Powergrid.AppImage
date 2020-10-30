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
from PyQt5.QtCore import Qt

from .device import DeviceWidget
from .label import Title
from .list import SettingsListWidget
from .text import DashboardDescription


class SettingsWidget(QtWidgets.QFrame):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @inject.params(service='plugin.service.hda')
    def __init__(self, service=None):
        super(SettingsWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(Title('Intel HDA'))
        self.layout().addWidget(DashboardDescription())

        self.list = SettingsListWidget()
        self.layout().addWidget(self.list)

        for device in service.devices():
            device_widget = DeviceWidget(device)
            device_widget.toggleDeviceAction.connect(self.toggleDeviceAction.emit)
            self.list.addWidget(device_widget)
