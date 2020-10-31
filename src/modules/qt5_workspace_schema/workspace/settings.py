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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .statistic import DashboardStatistic


class SettingsWidget(QtWidgets.QFrame):

    def __init__(self):
        super(SettingsWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.layout().addWidget(DashboardStatistic())

    def addWidget(self, widget):
        self.layout().addWidget(widget)
