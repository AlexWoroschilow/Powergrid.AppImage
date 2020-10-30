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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from .slider import DashboardSlider


class DashboardSettings(QtWidgets.QWidget):
    default_performance = None
    default_powersave = None

    @hexdi.inject('config')
    def __init__(self, config):
        self.default_performance = int(config.get('default.performance.watchdog', 1))
        self.default_powersave = int(config.get('default.powersave.watchdog', 0))
        super(DashboardSettings, self).__init__()


class DashboardSettingsPerformance(DashboardSettings):

    @hexdi.inject('config')
    def __init__(self, config):
        super(DashboardSettingsPerformance, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = int(config.get('watchdog.performance', self.default_performance))
        slider = DashboardSlider('Watchdog', int(value == self.default_performance))
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def action_slide(self, slider_state, config):
        value = self.default_powersave \
            if slider_state == 0 else \
            self.default_performance
        config.set('watchdog.performance', value)


class DashboardSettingsPowersave(DashboardSettings):

    @hexdi.inject('config')
    def __init__(self, config):
        super(DashboardSettingsPowersave, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = int(config.get('watchdog.powersave', self.default_powersave))
        slider = DashboardSlider('Watchdog', int(value == self.default_performance))
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def action_slide(self, slider_state, config):
        value = self.default_powersave \
            if slider_state == 0 else \
            self.default_performance
        config.set('watchdog.powersave', value)
