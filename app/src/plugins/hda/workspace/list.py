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
from .device import DeviceWidget

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class DeviceMonitorThread(QtCore.QThread):
    device = QtCore.pyqtSignal(object)

    @hexdi.inject('plugin.service.hda')
    def run(self, service=None):
        for device in service.devices():
            self.device.emit(device)


class SettingsListItem(QtWidgets.QListWidgetItem):

    def __init__(self, device=None):
        super(SettingsListItem, self).__init__()
        self.setSizeHint(QtCore.QSize(40, 30))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, device)


class SettingsListWidget(QtWidgets.QListWidget):
    toggleDeviceAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(SettingsListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setItemAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.thread = DeviceMonitorThread()
        self.thread.device.connect(self.addDevice)
        self.thread.start()

    def addDevice(self, device):
        item = SettingsListItem()
        self.addItem(item)

        widget = DeviceWidget(device)
        widget.toggleDeviceAction.connect(self.toggleDeviceAction.emit)
        self.setItemWidget(item, widget)
