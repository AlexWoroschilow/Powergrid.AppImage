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
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .label import DashboardTitle


class DashboardSchema(QtWidgets.QFrame):
    def __init__(self):
        super(DashboardSchema, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.update_text_event)
        self.timerRefresh.start(1000)

        self.content = DashboardTitle('Schema: ...')
        self.layout().addWidget(self.content)

    @hexdi.inject('plugin.service.watchdog')
    def update_text_event(self, service):
        for device in service.devices():
            value = 'powersave' \
                if device.power_control == '0' \
                else 'performance'
            self.content.setText('Schema: {}'.format(value))
            break
