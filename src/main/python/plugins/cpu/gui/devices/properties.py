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

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5 import QtCore

from .label import Title
from .label import Value
from .text import DashboardDescription
from .checkbox import CheckboxTriState


class DashboardPropertiesDeviceValue(Value):
    def __init__(self, device=None):
        super(DashboardPropertiesDeviceValue, self).__init__('')
        self.device = device

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.update_text_event)
        self.timerRefresh.start(1000)

    def update_text_event(self):
        return self.setText(' - <b>{}</b>, schema: <b>{}</b>'.format(
            self.device.name.replace('Cpu', 'CPU '), self.device.governor
        ))


class DashboardPropertiesDevice(QtWidgets.QWidget):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, device=None, config=None):
        super(DashboardPropertiesDevice, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.device = device

        default = config.get('cpu.permanent.{}'.format(self.device.code), 0)
        self.checkbox = CheckboxTriState(['Auto', 'Powersave', 'Performance'], int(default))
        self.checkbox.stateChanged.connect(self.toggle_device_event)

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.layout().addWidget(self.checkbox)
        self.layout().addWidget(DashboardPropertiesDeviceValue(device))

    @inject.params(config='config')
    def toggle_device_event(self, value, config):
        config.set('cpu.permanent.{}'.format(self.device.code), int(value))
        self.toggleDeviceAction.emit((value, self.device))


class DashboardProperties(QtWidgets.QFrame):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @inject.params(service='plugin.service.cpu')
    def __init__(self, service=None):
        super(DashboardProperties, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(Title('CPU - cores'))
        self.layout().addWidget(DashboardDescription())

        for device in sorted(service.cores()):
            device_widget = DashboardPropertiesDevice(device)
            device_widget.toggleDeviceAction.connect(self.toggleDeviceAction.emit)
            self.layout().addWidget(device_widget)