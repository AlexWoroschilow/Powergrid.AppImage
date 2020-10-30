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
import time

import inject
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .checkbox import CheckboxTriState
from .label import Value


class ThreadScanner(QtCore.QThread):
    status = QtCore.pyqtSignal(object)

    def __init__(self, device):
        super(ThreadScanner, self).__init__()
        self.device = device

    def run(self):
        if not self.device:
            return None

        while True:
            time.sleep(2)

            power_control = self.device.power_control
            self.status.emit("Not supported" if power_control is None else power_control)


class DeviceValueWidget(Value):
    def __init__(self, device=None):
        super(DeviceValueWidget, self).__init__('...')
        self.setAlignment(Qt.AlignVCenter)
        self.setMinimumWidth(120)

        self.thread = ThreadScanner(device)
        self.thread.status.connect(self.refreshEvent)
        self.thread.start()

    @inject.params(config='config')
    def refreshEvent(self, status, config):
        if status == config.get('i2c.powersave'):
            return self.setText("<b>{}</b>".format('powersave'))
        if status == config.get('i2c.performance'):
            return self.setText("<b>{}</b>".format('performance'))
        return self.setText("<b>{}</b>".format(status))


class DeviceWidget(QtWidgets.QWidget):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @inject.params(config='config')
    def __init__(self, device=None, config=None):
        super(DeviceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.device = device

        default = config.get('i2c.permanent.{}'.format(self.device.code), 0)
        self.checkbox = CheckboxTriState(['Auto', 'Powersave', 'Performance'], int(default))
        self.checkbox.stateChanged.connect(self.toggle_device_event)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.layout().addWidget(self.checkbox, 0, 0)
        self.layout().addWidget(DeviceValueWidget(device), 0, 1)
        self.layout().addWidget(QtWidgets.QLabel(device.name), 0, 2)

    @inject.params(config='config')
    def toggle_device_event(self, value, config):
        config.set('i2c.permanent.{}'.format(self.device.code), int(value))
        self.toggleDeviceAction.emit((value, self.device))
