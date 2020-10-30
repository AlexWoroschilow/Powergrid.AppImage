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
import inject

from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5 import QtGui
import psutil

from .label import DashboardStatisticTitle
from .painter import StatisticPainterCPUPercent
from .painter import StatisticPainterCPUFrequency
from .painter import StatisticPainterCPUFrequencyChart
from .painter import StatisticPainterBackground
from .painter import StatisticPainterGitter


class ThreadScanner(QtCore.QThread):
    core_temp = QtCore.pyqtSignal(object)
    core_percent = QtCore.pyqtSignal(object)
    battery_percent = QtCore.pyqtSignal(object)
    core = QtCore.pyqtSignal(object, object)

    @inject.params(service='plugin.service.cpu')
    def run(self, service=None):
        """

        :param service:
        :return:
        """

        while True:
            time.sleep(2)

            collection = [device.load for device in service.devices()]
            load = sum(collection) / len(collection)

            collection = [device.frequence for device in service.devices()]
            frequency = sum(collection) / len(collection)

            self.core.emit(frequency, load)

            # temperatures = psutil.sensors_temperatures()
            # collection = [x.current for x in temperatures['coretemp']]
            # self.core_temp.emit(sum(collection) / len(collection))
            #
            # percent = psutil.cpu_percent()
            # self.core_percent.emit(percent)
            #
            # battery = psutil.sensors_battery()
            # self.battery_percent.emit(battery.percent)


class StatisticChart(QtWidgets.QLabel):
    def __init__(self, width, height):
        super(StatisticChart, self).__init__()

        self.width = width
        self.height = height

        self.pixmap = QtGui.QPixmap(width, height)
        self.pixmap.fill(Qt.white)
        self.setPixmap(self.pixmap)

        self.painter_gitter = StatisticPainterGitter(self.pixmap)
        self.painter_background = StatisticPainterBackground(self.pixmap)
        self.painter_cpu_percent = StatisticPainterCPUPercent(self.pixmap)
        self.painter_cpu_frequency = StatisticPainterCPUFrequency(self.pixmap)
        self.painter_cpu_frequency_chart = StatisticPainterCPUFrequencyChart(self.pixmap)

        self.draw_cpu(0.0, 0.0)

    def draw_cpu(self, frequency, load):
        self.setPixmap(self.painter_background.refresh(frequency))
        self.setPixmap(self.painter_gitter.refresh(frequency))
        self.setPixmap(self.painter_cpu_frequency_chart.refresh(load if load <= 100 else 100))
        self.setPixmap(self.painter_cpu_frequency.refresh("{:.1f}".format(float(frequency) / 1000000)))
        self.setPixmap(self.painter_cpu_percent.refresh(load if load <= 100 else 100))


class DashboardStatistic(QtWidgets.QWidget):

    @inject.params(service='plugin.service.cpu')
    def __init__(self, service=None):
        super(DashboardStatistic, self).__init__()
        self.setMinimumHeight(250)

        self.setLayout(QtWidgets.QGridLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)

        self.chart = StatisticChart(self.width(), 250)
        self.layout().addWidget(self.chart, 18, 0, 2, 2)

        self.thread = ThreadScanner()
        self.thread.core.connect(self.chart.draw_cpu)
        #     self.thread.battery_percent.connect(self.update_value_battery_percent)
        self.thread.start()

    #
    # def update_value_core_temp(self, value=None):
    #     if value is None: return None
    #
    #     gauge = self.chart1.findChild(QtCore.QObject, 'performance')
    #     gauge.setProperty('load', int(value))
    #
    # def update_value_core_freq(self, value=None):
    #     (value)
    # if value is None: return None
    #
    # gauge = self.chart2.findChild(QtCore.QObject, 'title')
    # gauge.setProperty('title', "{:.1f} GHz".format(int(value) / 1000000))

    # def update_value_core_load(self, value=None):
    #     self.chart.draw_cpu_load("{:.1f}".format(int(value) / 1000000))
    #     if value is None: return None
    #
    #     gauge = self.chart2.findChild(QtCore.QObject, 'performance')
    #     gauge.setProperty('load', int(value))
    #
    # def update_value_core_percent(self, value=None):
    #     self.chart.draw_cpu_percent("{:.1f}".format(value))
    # if value is None: return None
    #
    #     gauge = self.chart4.findChild(QtCore.QObject, 'performance')
    #     gauge.setProperty('load', int(value))
    #
    #     gauge = self.chart4.findChild(QtCore.QObject, 'title')
    #     gauge.setProperty('title', "{:.1f} %".format(value))
    #
    # def update_value_battery_percent(self, value=None):
    #     if value is None: return None
    #
    #     gauge = self.chart3.findChild(QtCore.QObject, 'performance')
    #     gauge.setProperty('load', int(value))
