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

from .label import Field
from .label import Value


class DashboardProperties(QtWidgets.QWidget):
    @inject.params(service='plugin.service.watchdog')
    def __init__(self, service=None):
        super(DashboardProperties, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)

        self.layout().addWidget(Field('Current:'), 0, 0)

        for index, device in enumerate(service.devices(), start=1):
            current = '-' if device.power_control is None else device.power_control
            self.layout().addWidget(Value(current), 0, 1)
