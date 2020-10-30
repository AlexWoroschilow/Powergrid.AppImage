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

from .slider import DashboardSlider


class SettingsWidget(QtWidgets.QWidget):
    default_performance = None
    default_balanced = None
    default_powersave = None
    default_hashmap = None

    @inject.params(config='config')
    def __init__(self, config):
        super(SettingsWidget, self).__init__()
        self.default_performance = config.get('default.performance.sata', 'max_performance')
        self.default_balanced = config.get('default.balanced.sata', 'medium_power')
        self.default_powersave = config.get('default.powersave.sata', 'med_power_with_dipm')
        self.default_hashmap = {
            0: self.default_powersave,
            1: self.default_balanced,
            2: self.default_performance
        }


class SettingsPerformanceWidget(SettingsWidget):

    @inject.params(config='config')
    def __init__(self, config):
        super(SettingsPerformanceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        inverted = {self.default_hashmap[k]: k for k in self.default_hashmap}

        origin_performance = config.get('sata.performance', self.default_performance)
        if origin_performance not in inverted.keys(): return None

        slider = DashboardSlider('SATA', inverted[origin_performance])
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value not in self.default_hashmap.keys(): return None
        config.set('sata.performance', self.default_hashmap[value])


class SettingsPowersaveWidget(SettingsWidget):

    @inject.params(config='config')
    def __init__(self, config):
        super(SettingsPowersaveWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        inverted = {self.default_hashmap[k]: k for k in self.default_hashmap}

        origin_powersave = config.get('sata.powersave', self.default_powersave)
        if origin_powersave not in inverted.keys(): return None

        slider = DashboardSlider('SATA', inverted[origin_powersave])
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value not in self.default_hashmap.keys(): return None
        config.set('sata.powersave', self.default_hashmap[value])
