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
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui


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


class DashboardButtonFlat(PictureButton):
    def __init__(self, icon=None, text=None):
        super(DashboardButtonFlat, self).__init__(QtGui.QIcon(icon), None)
        self.setToolTipDuration(0)
        self.setToolTip(text)
        self.setText(text)
        self.setFlat(True)
