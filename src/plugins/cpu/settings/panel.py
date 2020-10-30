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

from plugins.cpu.settings.slider import DashboardSlider


class SettingsWidget(QtWidgets.QWidget):
    default_performance = None
    default_powersave = None

    @inject.params(config='config')
    def __init__(self, config):
        super(SettingsWidget, self).__init__()
        self.default_performance = config.get('default.performance.cpu', 'performance')
        self.default_powersave = config.get('default.powersave.cpu', 'powersave')


class SettingsPerformanceWidget(SettingsWidget):

    @inject.params(config='config')
    def __init__(self, config):
        super(SettingsPerformanceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('cpu.performance', self.default_performance)
        slider = DashboardSlider('CPU', self.governors, value)
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @property
    @inject.params(service='plugin.service.cpu')
    def governors(self, service=None):
        for device in service.devices():
            return sorted(device.governors, reverse=True)
        return []

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value is None: return None
        config.set('cpu.performance', value)


class SettingsPowersaveWidget(SettingsWidget):

    @inject.params(config='config')
    def __init__(self, config):
        super(SettingsPowersaveWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('cpu.powersave', self.default_powersave)
        slider = DashboardSlider('CPU', self.governors, value)
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @property
    @inject.params(service='plugin.service.cpu')
    def governors(self, service=None):
        for device in service.devices():
            return sorted(device.governors, reverse=True)
        return []

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value is None: return None
        config.set('cpu.powersave', value)
