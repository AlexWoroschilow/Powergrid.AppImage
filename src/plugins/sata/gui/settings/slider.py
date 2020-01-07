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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

from PyQt5 import QtCore
from PyQt5 import QtGui

from .label import Value
from .label import Title


class DashboardSlider(QtWidgets.QWidget):
    slideAction = QtCore.pyqtSignal(object)

    def __init__(self, name, value):
        super(DashboardSlider, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setAlignment(Qt.AlignCenter)

        self.slider = QtWidgets.QSlider(Qt.Vertical)
        self.slider.valueChanged.connect(self.action_slide)
        self.slider.setTickPosition(QtWidgets.QSlider.TicksLeft)
        self.slider.setValue(int(value))
        self.slider.setMaximum(2)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)

        self.layout().addWidget(self.slider, 0, 1, 1, 1)
        self.layout().addWidget(Title(name), 1, 0, 1, 3)

    def action_slide(self, index=None):
        self.slideAction.emit(index)
