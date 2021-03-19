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

import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .checkbox import CheckboxTriState


class ThreadScanner(QtCore.QThread):
    powerPolicyAction = QtCore.pyqtSignal(object)
    powerControlAction = QtCore.pyqtSignal(object)

    def __init__(self, device):
        super(ThreadScanner, self).__init__()
        self.device = device

    def run(self):
        if not self.device:
            return None

        while True:
            time.sleep(2)

            self.powerControlAction.emit(self.device.power_control)
            self.powerPolicyAction.emit(self.device.policy)


class DeviceValueWidget(QtWidgets.QWidget):
    def __init__(self, device=None):
        super(DeviceValueWidget, self).__init__()
        self.setContentsMargins(0, 0, 0, 0)

        self.thread = ThreadScanner(device)
        self.thread.powerPolicyAction.connect(self.powerPolicyEvent)
        self.thread.powerControlAction.connect(self.powerControlEvent)
        self.thread.start()

        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.power_policy = QtWidgets.QLabel('...')
        self.power_policy.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.layout().addWidget(self.power_policy)

        self.power_control = QtWidgets.QLabel('...')
        self.power_control.setAlignment(Qt.AlignVCenter | Qt.AlignCenter)
        self.layout().addWidget(self.power_control)

    def powerPolicyEvent(self, status):
        return self.power_policy.setText("<b>{}</b>".format(status))

    def powerControlEvent(self, status):
        return self.power_control.setText("<b>{}</b>".format(status))


class DeviceWidget(QtWidgets.QWidget):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    @hexdi.inject('config')
    def __init__(self, device=None, config=None):
        super(DeviceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.setContentsMargins(0, 0, 0, 0)
        self.setToolTip(device.path)

        self.device = device

        default = config.get('sata.permanent.{}'.format(self.device.code), 0)
        self.checkbox = CheckboxTriState(['Auto', 'Powersave', 'Performance'], int(default))
        self.checkbox.stateChanged.connect(self.toggle_device_event)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignLeft | Qt.AlignTop)

        self.layout().addWidget(self.checkbox, 0, 0)
        self.layout().addWidget(DeviceValueWidget(device), 0, 1)
        self.layout().addWidget(QtWidgets.QLabel(device.name), 0, 2)

    @hexdi.inject('config')
    def toggle_device_event(self, value, config):
        config.set('sata.permanent.{}'.format(self.device.code), int(value))
        self.toggleDeviceAction.emit((value, self.device))
