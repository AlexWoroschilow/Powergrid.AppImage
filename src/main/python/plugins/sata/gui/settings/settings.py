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
    hashmap = {
        0: 'min_power',
        1: 'medium_power',
        2: 'max_performance'
    }

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettingsPerformance, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        inverted = {self.hashmap[k]: k for k in self.hashmap}

        origin_performance = config.get('sata.performance', 'max_performance')
        if origin_performance not in inverted.keys(): return None

        slider = DashboardSlider('SATA', inverted[origin_performance])
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value not in self.hashmap.keys(): return None
        config.set('sata.performance', self.hashmap[value])


class DashboardSettingsPowersave(QtWidgets.QWidget):
    hashmap = {
        0: 'min_power',
        1: 'medium_power',
        2: 'max_performance'
    }

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettingsPowersave, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        inverted = {self.hashmap[k]: k for k in self.hashmap}

        origin_powersave = config.get('sata.powersave', 'min_power')
        if origin_powersave not in inverted.keys(): return None

        slider = DashboardSlider('SATA', inverted[origin_powersave])
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, value, config):
        if value not in self.hashmap.keys(): return None
        config.set('sata.powersave', self.hashmap[value])
