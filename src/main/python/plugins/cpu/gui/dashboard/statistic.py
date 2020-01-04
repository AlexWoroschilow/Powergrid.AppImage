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
import psutil


class DashboardSchemaContainer(QtWidgets.QFrame):
    @inject.params(service='plugin.service.cpu')
    def __init__(self, service=None):
        super(DashboardSchemaContainer, self).__init__()
        self.setLayout(QtWidgets.QGridLayout())
        self.setMinimumHeight(100)

        self.charts = {}

        i, j = 0, 0
        for index, device in enumerate(sorted(service.cores()), start=0):
            chart = QtQuick.QQuickView()
            chart.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
            chart.setSource(QtCore.QUrl('charts/gauge-short.qml'))

            content = QtWidgets.QWidget.createWindowContainer(chart, self)
            content.setMinimumSize(QtCore.QSize(80, 80))
            self.layout().addWidget(content, i, j)
            i = i if j < 3 else i + 1
            j = j + 1 if j < 3 else 0

            self.charts[index] = chart

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.update_value)
        self.timerRefresh.start(3000)

    @inject.params(service='plugin.service.cpu')
    def update_value(self, service=None):
        for index, device in enumerate(sorted(service.cores()), start=0):
            if index not in self.charts.keys():
                continue
            chart = self.charts[index]

            gauge = chart.findChild(QtCore.QObject, 'title')
            gauge.setProperty('title', device.name.replace('Cpu', 'CPU '))

            gauge = chart.findChild(QtCore.QObject, 'performance')
            gauge.setProperty('load', round(device.load, 1))


class DashboardImage(QtWidgets.QWidget):

    @inject.params(service='plugin.service.cpu')
    def __init__(self, service=None):
        super(DashboardImage, self).__init__()

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.chart1 = QtQuick.QQuickView()
        self.chart1.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.chart1.setSource(QtCore.QUrl("charts/gauge-left-side.qml"))

        contianer = QtWidgets.QWidget.createWindowContainer(self.chart1, self)
        contianer.setMinimumSize(QtCore.QSize(110, 110))
        self.layout().addWidget(contianer, 18, 0, 2, 2)

        self.chart2 = QtQuick.QQuickView()
        self.chart2.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.chart2.setSource(QtCore.QUrl("charts/gauge-left.qml"))

        contianer = QtWidgets.QWidget.createWindowContainer(self.chart2, self)
        contianer.setMinimumSize(QtCore.QSize(200, 200))
        self.layout().addWidget(contianer, 0, 1, 20, 20)

        self.chart3 = QtQuick.QQuickView()
        self.chart3.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.chart3.setSource(QtCore.QUrl("charts/gauge-right-side.qml"))

        contianer = QtWidgets.QWidget.createWindowContainer(self.chart3, self)
        contianer.setMinimumSize(QtCore.QSize(110, 110))
        self.layout().addWidget(contianer, 18, 40, 2, 2)

        self.chart4 = QtQuick.QQuickView()
        self.chart4.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.chart4.setSource(QtCore.QUrl("charts/gauge-right.qml"))

        contianer = QtWidgets.QWidget.createWindowContainer(self.chart4, self)
        contianer.setMinimumSize(QtCore.QSize(200, 200))
        self.layout().addWidget(contianer, 0, 21, 20, 20)

        self.timerRefresh = QtCore.QTimer()
        self.timerRefresh.timeout.connect(self.update_value)
        self.timerRefresh.start(2000)

    @inject.params(service='plugin.service.cpu')
    def update_value(self, service=None):
        collection = [device.load for device in service.cores()]
        gauge = self.chart2.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', sum(collection) / len(collection))

        collection = [device.frequence for device in service.cores()]
        gauge = self.chart2.findChild(QtCore.QObject, 'title')
        gauge.setProperty('title', "{:.1f} GHz".format(sum(collection) / len(collection) / 1000000))

        load = psutil.cpu_percent()
        gauge = self.chart4.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', load)

        gauge = self.chart4.findChild(QtCore.QObject, 'title')
        gauge.setProperty('title', "{:.1f} %".format(load))

        battery = psutil.sensors_battery()
        gauge = self.chart3.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', battery.percent)

        temperatures = psutil.sensors_temperatures()
        collection = [x.current for x in temperatures['coretemp']]
        gauge = self.chart1.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', sum(collection) / len(collection))
