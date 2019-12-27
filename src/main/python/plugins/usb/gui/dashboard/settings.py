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
import copy
import hexdi
import webbrowser

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtGui

from .slider import DashboardSlider


class DashboardSettings(QtWidgets.QWidget):

    @hexdi.inject('config')
    def __init__(self, config):
        super(DashboardSettings, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())

        value = config.get('usb.performance', 'on')
        slider1 = DashboardSlider('AC- Adapter', int(value == 'on'))
        self.layout().addWidget(slider1, 0, 0)

        value = config.get('usb.powersave', 'auto')
        slider2 = DashboardSlider('Battery', int(value == 'on'))
        self.layout().addWidget(slider2, 1, 0)

        slider1.slideAction.connect(self.actionSlidePerformance)
        slider2.slideAction.connect(self.actionSlidePowersave)

    @hexdi.inject('config')
    def actionSlidePerformance(self, value, config):
        if value is None: return None
        config.set('usb.performance', 'on' if value == 1 else 'auto')
        config.set('usb.performance.power_level', 'on' if value == 1 else 'auto')
        config.set('usb.performance.power_control', 'on' if value == 1 else 'auto')
        config.set('usb.performance.autosuspend_delay', '-1' if value == 1 else '500')
        config.set('usb.performance.autosuspend', '-1' if value == 1 else '500')

    @hexdi.inject('config')
    def actionSlidePowersave(self, value, config):
        if value is None: return None
        config.set('usb.powersave', 'on' if value == 1 else 'auto')
        config.set('usb.powersave.power_level', 'on' if value == 1 else 'auto')
        config.set('usb.powersave.power_control', 'on' if value == 1 else 'auto')
        config.set('usb.powersave.autosuspend_delay', '-1' if value == 1 else '500')
        config.set('usb.powersave.autosuspend', '-1' if value == 1 else '500')
