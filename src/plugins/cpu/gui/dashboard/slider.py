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


class DashboardSlider(QtWidgets.QWidget):
    slideAction = QtCore.pyqtSignal(object)

    def __init__(self, name, values, value):
        self.values = values

        super(DashboardSlider, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.setLayout(QtWidgets.QGridLayout())

        self.layout().addWidget(Title(name), 0, 0, 1, len(values))

        self.slider = QtWidgets.QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QtWidgets.QSlider.NoTicks)
        self.slider.valueChanged.connect(self.actionSlide)
        if values is not None and value in values:
            self.slider.setValue(values.index(value))

        self.slider.setMaximum(len(self.values) - 1)
        self.slider.setSingleStep(1)
        self.slider.setMinimum(0)

        self.layout().addWidget(self.slider, 1, 0, 1, len(values))

        for index, value in enumerate(self.values, start=0):
            align = Qt.AlignLeft if index < (len(self.values) / 2) else Qt.AlignRight

            value = Value(value.capitalize())
            value.setAlignment(align)

            self.layout().addWidget(value, 2, index)

    def actionSlide(self, index=None):
        if index is None: return None
        self.slideAction.emit(self.values[index])