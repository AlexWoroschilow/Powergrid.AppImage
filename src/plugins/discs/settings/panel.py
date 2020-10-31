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


class SettingsWidget(QtWidgets.QWidget):
    default_performance = None
    default_powersave = None

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsWidget, self).__init__()
        self.default_performance = config.get('default.performance.disc')
        self.default_powersave = config.get('default.powersave.disc')

    def getValueInternal(self, value):
        if value == self.default_powersave: return 0
        if value == self.default_performance: return 1
        return 0

    def getValueExternal(self, value):
        if value == 0: return self.default_powersave
        if value == 1: return self.default_performance
        return self.default_powersave


class SettingsPerformanceWidget(SettingsWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsPerformanceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('disc.performance', self.default_performance)
        slider = DashboardSlider('Disc', self.getValueInternal(value))
        slider.slideAction.connect(self.slideEvent)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def slideEvent(self, value, config):
        config.set('disc.performance', self.getValueExternal(value))


class SettingsPowersaveWidget(SettingsWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsPowersaveWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('disc.powersave', self.default_powersave)
        slider = DashboardSlider('Disc', self.getValueInternal(value))
        slider.slideAction.connect(self.slideEvent)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def slideEvent(self, value, config):
        config.set('disc.powersave', self.getValueExternal(value))
