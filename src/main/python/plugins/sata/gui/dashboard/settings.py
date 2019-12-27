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

from .slider import DashboardSlider


class DashboardSettings(QtWidgets.QWidget):
    hashmap = {
        0: 'min_power',
        1: 'medium_power',
        2: 'max_performance'
    }

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettings, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())

        inverted = {self.hashmap[k]: k for k in self.hashmap}

        origin_performance = config.get('sata.performance', 'max_performance')
        if origin_performance not in inverted.keys(): return None

        slider1 = DashboardSlider('AC- Adapter', inverted[origin_performance])
        slider1.slideAction.connect(self.actionSlidePerformance)

        origin_powersave = config.get('sata.powersave', 'min_power')
        if origin_powersave not in inverted.keys(): return None

        slider2 = DashboardSlider('Battery', inverted[origin_powersave])
        slider2.slideAction.connect(self.actionSlidePowersave)

        self.layout().addWidget(slider1, 0, 0)
        self.layout().addWidget(slider2, 1, 0)

    @inject.params(config='config')
    def actionSlidePerformance(self, value, config):
        if value not in self.hashmap.keys(): return None

        config.set('sata.performance', self.hashmap[value])

    @inject.params(config='config')
    def actionSlidePowersave(self, value, config):
        if value not in self.hashmap.keys(): return None

        config.set('sata.powersave', self.hashmap[value])
