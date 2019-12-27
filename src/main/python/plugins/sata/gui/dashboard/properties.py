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
import hexdi
import itertools

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .label import Field
from .label import Value
from PyQt5 import QtCore


class DashboardPropertiesDeviceValue(Value):
    def __init__(self, device=None):
        super(DashboardPropertiesDeviceValue, self).__init__('Scheme: <b>unknown</b>, uncheck to ignore ')
        self.device = device

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.updateTextEvent)
        self.timerRefresh.start(1000)

    def updateTextEvent(self):
        value = self.device.power_control
        if value is None or not len(value): return None
        self.setText('Scheme: <b>{}</b>, uncheck to ignore '.format(value))


class DashboardPropertiesDevice(QtWidgets.QWidget):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, device=None, config=None):
        super(DashboardPropertiesDevice, self).__init__()
        self.device = device

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft)

        self.layout().addWidget(DashboardPropertiesDeviceValue(device), 0, 0)

        self.checkbox = QtWidgets.QCheckBox(device.name.replace('Host', 'Host '))
        self.checkbox.setChecked(int(config.get('sata.managed.{}'.format(self.device.code), 1)))
        self.checkbox.stateChanged.connect(self.toggleDeviceEvent)

        self.layout().addWidget(self.checkbox, 0, 1)

    @hexdi.inject('config')
    def toggleDeviceEvent(self, value, config):
        self.toggleDeviceAction.emit((value, self.device))
        config.set('sata.managed.{}'.format(self.device.code), int(value != 0))


class DashboardProperties(QtWidgets.QFrame):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @hexdi.inject('plugin.service.sata')
    def __init__(self, service=None):
        super(DashboardProperties, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter | Qt.AlignTop)

        for device in service.cores():
            self.layout().addWidget(DashboardPropertiesDevice(device))
