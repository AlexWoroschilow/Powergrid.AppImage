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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .device import DeviceWidget


class DeviceMonitorThread(QtCore.QThread):
    addAction = QtCore.pyqtSignal(object)
    removeAction = QtCore.pyqtSignal(object)

    @hexdi.inject('plugin.service.disc')
    def run(self, service=None):

        for device in service.devices():
            self.addAction.emit(device)

        for device in service.monitor():
            if device.action in ['add']:
                self.addAction.emit(device)


class SettingsListItem(QtWidgets.QListWidgetItem):

    def __init__(self, device=None):
        super(SettingsListItem, self).__init__()
        self.setSizeHint(QtCore.QSize(40, 30))
        self.setTextAlignment(Qt.AlignCenter)
        self.setData(0, device)


class SettingsListWidget(QtWidgets.QListWidget):
    deviceToggleAction = QtCore.pyqtSignal(object)
    deviceRemoveAction = QtCore.pyqtSignal(object)

    def __init__(self):
        super(SettingsListWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self._hashmap = {}

        self.thread = DeviceMonitorThread()
        self.thread.addAction.connect(self.addDevice)
        self.thread.removeAction.connect(self.removeDevice)
        self.thread.start()

    def addDevice(self, device):
        if device.code in self._hashmap.keys():
            return self

        item = SettingsListItem()
        self.addItem(item)

        widget = DeviceWidget(device)
        widget.deviceToggleAction.connect(self.deviceToggleAction.emit)
        widget.deviceRemoveAction.connect(self.removeDevice)
        self.setItemWidget(item, widget)

        self._hashmap[device.code] = item

    def removeDevice(self, device):
        if device.code not in self._hashmap.keys():
            return self

        item = self._hashmap[device.code]
        del self._hashmap[device.code]

        self.takeItem(self.row(item))
