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
        self.default_performance = int(config.get('default.performance.hda', 0))
        self.default_powersave = int(config.get('default.powersave.hda', 5))


class SettingsPerformanceWidget(SettingsWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsPerformanceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        value = int(config.get('hda.performance', self.default_performance))
        slider = DashboardSlider('HDA', int(value == self.default_performance))
        slider.slideAction.connect(self.action_slide)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def action_slide(self, slider_position, config):
        value = self.default_powersave \
            if slider_position == 0 else \
            self.default_performance

        config.set('hda.performance', value)


class SettingsPowersaveWidget(SettingsWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsPowersaveWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        value = int(config.get('hda.powersave', self.default_powersave))
        slider = DashboardSlider('HDA', int(value == self.default_performance))
        slider.slideAction.connect(self.action_slide)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def action_slide(self, slider_position, config):
        value = self.default_powersave \
            if slider_position == 0 else \
            self.default_performance

        config.set('hda.powersave', value)
