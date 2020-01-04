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

from PyQt5 import QtCore
from PyQt5 import QtGui

from .slider import DashboardSlider


class DashboardSettingsPerformance(QtWidgets.QWidget):

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettingsPerformance, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('watchdog.performance', '1')
        slider = DashboardSlider('Watchdog', 0 if value == '0' else 1)
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value is None: return None
        config.set('watchdog.performance', '0' if value == 0 else '1')


class DashboardSettingsPowersave(QtWidgets.QWidget):

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettingsPowersave, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('watchdog.powersave', '0')
        slider = DashboardSlider('Watchdog', 0 if value == '0' else 1)
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value is None: return None
        config.set('watchdog.powersave', '0' if value == 0 else '1')
