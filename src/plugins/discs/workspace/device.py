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
import functools
import os
import time

import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .checkbox import CheckboxTriState
from .label import Value


class ThreadScanner(QtCore.QThread):
    deviceRemoveAction = QtCore.pyqtSignal(object)
    deviceStatusAction = QtCore.pyqtSignal(object)

    def __init__(self, device):
        super(ThreadScanner, self).__init__()
        self.device = device

    def run(self):
        if not self.device:
            return None

        while True:
            time.sleep(2)
            if not os.path.exists(self.device.path):
                self.deviceRemoveAction.emit(self.device)
                continue

            if not self.device.power_control:
                self.deviceStatusAction.emit("Not supported")
                continue

            self.deviceStatusAction.emit(self.device.power_control)


class DeviceValueWidget(Value):
    deviceRemoveAction = QtCore.pyqtSignal(object)

    def __init__(self, device=None):
        super(DeviceValueWidget, self).__init__('...')
        self.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.setMinimumWidth(80)

        self.thread = ThreadScanner(device)
        self.thread.deviceRemoveAction.connect(self.deviceRemoveAction)
        self.thread.deviceRemoveAction.connect(self.thread.exit)
        self.thread.deviceStatusAction.connect(self.refreshEvent)
        self.thread.start()

    def refreshEvent(self, status):
        return self.setText("<b>{}</b>".format(status))


class DeviceWidget(QtWidgets.QWidget):
    deviceToggleAction = QtCore.pyqtSignal(object)
    deviceRemoveAction = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, device=None, config=None):
        super(DeviceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.checkbox = CheckboxTriState([
            'Auto', 'Powersave', 'Performance'
        ], int(config.get('disc.permanent.{}'.format(device.code), 0)))
        self.checkbox.stateChanged.connect(functools.partial(
            self.deviceToggleEvent, device
        ))
        self.layout().addWidget(self.checkbox, 0, 0)

        self.name = DeviceValueWidget(device)
        self.name.deviceRemoveAction.connect(self.deviceRemoveAction.emit)
        self.layout().addWidget(self.name, 0, 1)

        self.layout().addWidget(QtWidgets.QLabel(device.name), 0, 2)

    @hexdi.inject('config')
    def deviceToggleEvent(self, device, value, config):
        config.set('disc.permanent.{}'.format(device.code), int(value))
        self.deviceToggleAction.emit((value, device))
