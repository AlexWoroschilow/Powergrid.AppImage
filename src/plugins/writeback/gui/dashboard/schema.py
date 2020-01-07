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

from .label import DashboardTitle


class DashboardSchema(QtWidgets.QFrame):

    def __init__(self):
        super(DashboardSchema, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.update_text_event)
        self.timerRefresh.start(1000)

        self.content = DashboardTitle('Schema: ...')
        self.content.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.content.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.content)

    @property
    @inject.params(service='plugin.service.writeback')
    def writeback(self, service=None):
        for device in service.devices():
            return int(device.power_control)

    @inject.params(config='config')
    def update_text_event(self, config=None):
        performance = config.get('writeback.performance', '500')
        powersave = config.get('writeback.powersave', '1500')

        hashmap = {
            int(performance)
            if len(performance) else
            500: "performance",
            int(powersave)
            if len(performance) else
            500: "powersave",
        }

        writeback = self.writeback

        value = hashmap[writeback] \
            if writeback in hashmap.keys() \
            else "Unknown"

        writeback = writeback / 100 \
            if int(writeback) > 0 else 0

        return self.content.setText('Schema: {} ({:.0f} sec)'.format(value, writeback))
