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
import time

import hexdi
import psutil
from PyQt5 import QtCore
from PyQt5 import QtQuick
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class ThreadScanner(QtCore.QThread):
    core_temp = QtCore.pyqtSignal(object)
    core_load = QtCore.pyqtSignal(object)
    core_freq = QtCore.pyqtSignal(object)
    core_percent = QtCore.pyqtSignal(object)
    battery_percent = QtCore.pyqtSignal(object)

    @hexdi.inject('plugin.service.cpu')
    def run(self, service=None):
        """

        :param service:
        :return:
        """

        while True:
            time.sleep(2)

            collection = [device.load for device in service.cores()]
            self.core_load.emit(sum(collection) / len(collection))

            collection = [device.frequence for device in service.cores()]
            self.core_freq.emit(sum(collection) / len(collection))

            temperatures = psutil.sensors_temperatures()
            collection = [x.current for x in temperatures['coretemp']]
            self.core_temp.emit(sum(collection) / len(collection))

            percent = psutil.cpu_percent()
            self.core_percent.emit(percent)

            battery = psutil.sensors_battery()
            self.battery_percent.emit(battery.percent)


class DashboardImage(QtWidgets.QWidget):

    @hexdi.inject('plugin.service.cpu')
    def __init__(self, service=None):
        super(DashboardImage, self).__init__()
        self.setMinimumHeight(250)

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

        self.thread = ThreadScanner()
        self.thread.core_temp.connect(self.update_value_core_temp)
        self.thread.core_load.connect(self.update_value_core_load)
        self.thread.core_freq.connect(self.update_value_core_freq)
        self.thread.core_percent.connect(self.update_value_core_percent)
        self.thread.battery_percent.connect(self.update_value_battery_percent)
        self.thread.start()

    def update_value_core_temp(self, value=None):
        if value is None: return None

        gauge = self.chart1.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', int(value))

    def update_value_core_freq(self, value=None):
        if value is None: return None

        gauge = self.chart2.findChild(QtCore.QObject, 'title')
        gauge.setProperty('title', "{:.1f} GHz".format(int(value) / 1000000))

    def update_value_core_load(self, value=None):
        if value is None: return None

        gauge = self.chart2.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', int(value))

    def update_value_core_percent(self, value=None):
        if value is None: return None

        gauge = self.chart4.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', int(value))

        gauge = self.chart4.findChild(QtCore.QObject, 'title')
        gauge.setProperty('title', "{:.1f} %".format(value))

    def update_value_battery_percent(self, value=None):
        if value is None: return None

        gauge = self.chart3.findChild(QtCore.QObject, 'performance')
        gauge.setProperty('load', int(value))
