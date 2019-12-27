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

from .label import Title
from .label import Value


class DashboardSlider(QtWidgets.QFrame):
    slideAction = QtCore.pyqtSignal(object)

    def __init__(self, name, value):
        super(DashboardSlider, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())

        self.layout().addWidget(Title(name), 0, 0, 1, 4)

        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.layout().addWidget(self.slider, 1, 0, 1, 4)
        self.slider.valueChanged.connect(self.actionSlide)
        self.slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider.setValue(int(value))
        self.slider.setMaximum(1)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)

        label = Value('powersave')
        label.setAlignment(Qt.AlignLeft)
        self.layout().addWidget(label, 2, 0)

        label = Value('performance')
        label.setAlignment(Qt.AlignRight)
        self.layout().addWidget(label, 2, 3)

    def actionSlide(self, index=None):
        self.slideAction.emit(index)
