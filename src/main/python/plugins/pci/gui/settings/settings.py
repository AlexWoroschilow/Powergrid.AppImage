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


class DashboardSettings(QtWidgets.QWidget):
    default_performance = None
    default_powersave = None

    @inject.params(config='config')
    def __init__(self, config):
        """
        The time-out for automatic power-off can be specified via power_save module option of snd-ac97-codec
        and snd-hda-intel modules. Specify the time-out value in seconds. 0 means to disable the automatic power-saving.
        The default value of timeout is given via CONFIG_SND_AC97_POWER_SAVE_DEFAULT and CONFIG_SND_HDA_POWER_SAVE_DEFAULT Kconfig options.
        Setting this to 1 (the minimum value) isn’t recommended because many applications try to reopen the device frequently.
        10 would be a good choice for normal operations.
        :param config:
        """
        self.default_performance = config.get('default.performance.pci', 'on')
        self.default_powersave = config.get('default.powersave.pci', 'auto')
        super(DashboardSettings, self).__init__()


class DashboardSettingsPerformance(DashboardSettings):

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettingsPerformance, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('pci.performance', self.default_performance)
        slider = DashboardSlider('PCI', int(value == self.default_performance))
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, slider_state, config):
        value = self.default_powersave \
            if slider_state == 0 else \
            self.default_performance
        config.set('pci.performance', value)


class DashboardSettingsPowersave(DashboardSettings):

    @inject.params(config='config')
    def __init__(self, config):
        super(DashboardSettingsPowersave, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        value = config.get('pci.powersave', self.default_powersave)
        slider = DashboardSlider('PCI', int(value == self.default_performance))
        slider.slideAction.connect(self.action_slide)

        self.layout().addWidget(slider)

    @inject.params(config='config')
    def action_slide(self, slider_state, config):
        value = self.default_powersave \
            if slider_state == 0 else \
            self.default_performance
        config.set('pci.powersave', value)
