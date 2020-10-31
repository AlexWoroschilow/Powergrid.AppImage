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
    default_balanced = None
    default_powersave = None
    default_hashmap = None

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsWidget, self).__init__()
        self.default_performance_policy = config.get('default.performance.sata.policy', 'max_performance')
        self.default_balanced_policy = config.get('default.balanced.sata.policy', 'med_power_with_dipm')
        self.default_powersave_policy = config.get('default.powersave.sata.policy', 'min_power')

        self.default_performance_control = config.get('default.performance.sata.control', 'on')
        self.default_powersave_control = config.get('default.powersave.sata.control', 'auto')

    def getValueInternal(self, value):
        if value == self.default_powersave_policy: return 0
        if value == self.default_balanced_policy: return 1
        if value == self.default_performance_policy: return 2
        return 0

    def getValuePolicy(self, value):
        if value == 0: return self.default_powersave_policy
        if value == 1: return self.default_balanced_policy
        if value == 2: return self.default_performance_policy
        return self.default_balanced_policy

    def getValueControl(self, value):
        if value == 0: return self.default_powersave_control
        if value == 1: return self.default_performance_control
        if value == 2: return self.default_performance_control
        return self.default_powersave_control


class SettingsPerformanceWidget(SettingsWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsPerformanceWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value_current = config.get('sata.performance.policy', self.default_performance_policy)
        slider = DashboardSlider('SATA', self.getValueInternal(value_current))
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def action_slide(self, value, config):
        print(self.getValuePolicy(value), self.getValueControl(value))
        config.set('sata.performance.policy', self.getValuePolicy(value))
        config.set('sata.performance.control', self.getValueControl(value))


class SettingsPowersaveWidget(SettingsWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(SettingsPowersaveWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value_current = config.get('sata.powersave.policy', self.default_powersave_policy)
        slider = DashboardSlider('SATA', self.getValueInternal(value_current))
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @hexdi.inject('config')
    def action_slide(self, value, config):
        config.set('sata.powersave.policy', self.getValuePolicy(value))
        config.set('sata.powersave.control', self.getValueControl(value))
