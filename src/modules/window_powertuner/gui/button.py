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
import os
import functools

from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


class ButtonDisabled(QtWidgets.QPushButton):

    def __init__(self, icon=None, text=None):
        super(ButtonDisabled, self).__init__(icon, None)
        self.setCheckable(False)
        self.setFlat(True)
        self.setDisabled(True)


class PictureButton(QtWidgets.QPushButton):
    def __init__(self, icon=None, text=None):
        super(PictureButton, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setToolTip(text)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.Enter:
            effect = QtWidgets.QGraphicsDropShadowEffect()
            effect.setColor(QtGui.QColor('#6cccfc'))
            effect.setBlurRadius(5)
            effect.setOffset(0)
            self.setGraphicsEffect(effect)

        if QEvent.type() == QtCore.QEvent.Leave:
            self.setGraphicsEffect(None)

        return super(PictureButton, self).event(QEvent)


class PictureButtonFlat(PictureButton):
    def __init__(self, icon=None, text=None):
        super(PictureButtonFlat, self).__init__(icon, None)
        self.setToolTipDuration(0)
        self.setToolTip(text)
        self.setFlat(True)


class CPUButtonFlat(PictureButton):
    def __init__(self, icon=None, text=None):
        super(CPUButtonFlat, self).__init__(icon, None)
        self.setDisabled(not os.path.exists('/etc/performance-tuner'))
        self.setToolTipDuration(0)
        self.setToolTip(text)
        self.setFlat(True)
