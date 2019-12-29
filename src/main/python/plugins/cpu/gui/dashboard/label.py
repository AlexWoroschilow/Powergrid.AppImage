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

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtQuick


class DashboardImage(QtWidgets.QWidget):

    @inject.params(service='plugin.service.cpu')
    def __init__(self, image=None, service=None):
        super(DashboardImage, self).__init__()
        self.setMinimumWidth(200)

        self.setLayout(QtWidgets.QVBoxLayout())

        self.chart = QtQuick.QQuickView()
        self.chart.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)

        self.chart.setSource(QtCore.QUrl("charts/gauge.qml"))
        self.layout().addWidget(QtWidgets.QWidget.createWindowContainer(self.chart, self))

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.update_value)
        self.timerRefresh.start(1000)

    @inject.params(service='plugin.service.cpu')
    def update_value(self, service=None):
        collection = [device.load for device in service.cores()]
        gauge = self.chart.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', sum(collection) / len(collection))


class DashboardTitle(QtWidgets.QLabel):

    def __init__(self, text):
        super(DashboardTitle, self).__init__(text)
        self.setAlignment(Qt.AlignLeft)
        self.setWordWrap(True)


class Title(QtWidgets.QLabel):

    def __init__(self, text):
        super(Title, self).__init__(text)
        self.setAlignment(Qt.AlignCenter)
        self.setWordWrap(True)


class Field(QtWidgets.QLabel):

    def __init__(self, text):
        super(Field, self).__init__(text)
        self.setAlignment(Qt.AlignLeft)


class Value(QtWidgets.QLabel):

    def __init__(self, text):
        super(Value, self).__init__(text)
        self.setAlignment(Qt.AlignLeft)
