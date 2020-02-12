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
from PyQt5 import QtQuick
import psutil

from .label import DashboardStatisticTitle


class StatisticPainterAbstract(object):
    def __init__(self, pixmap):
        self.width = pixmap.width()
        self.height = pixmap.height()
        self.pixmap = pixmap
        self.text_rect = None

    def get_relative_height(self, percent):
        return self.height / 100 * percent

    def get_relative_width(self, percent):
        return self.width / 100 * percent


class StatisticPainterCPUPercent(StatisticPainterAbstract):
    def __init__(self, pixmap):
        super(StatisticPainterCPUPercent, self).__init__(pixmap)

    def refresh(self, value):
        painter = QtGui.QPainter()
        painter.begin(self.pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)

        text = "{:.1f} %".format(value)

        painter.setFont(QtGui.QFont('Tahoma', 30))
        painter.setPen(QtGui.QPen(QtGui.QColor('#e0e0e0')))
        painter.drawText(self.get_relative_width(55.5),
                         self.get_relative_height(68), text)

        painter.setFont(QtGui.QFont('Tahoma', 30))
        painter.setPen(QtGui.QPen(QtGui.QColor('#000000')))
        painter.drawText(self.get_relative_width(55),
                         self.get_relative_height(70), text)

        text = "CPU load"

        painter.setFont(QtGui.QFont('Tahoma', 15))
        painter.setPen(QtGui.QPen(QtGui.QColor('#e0e0e0')))
        painter.drawText(self.get_relative_width(57.5),
                         self.get_relative_height(78), text)

        painter.setFont(QtGui.QFont('Tahoma', 15))
        painter.setPen(QtGui.QPen(QtGui.QColor('#000000')))
        painter.drawText(self.get_relative_width(57),
                         self.get_relative_height(80), text)

        painter.end()

        return self.pixmap


class StatisticPainterCPUFrequency(StatisticPainterAbstract):
    def __init__(self, pixmap):
        super(StatisticPainterCPUFrequency, self).__init__(pixmap)

    def refresh(self, value):
        painter = QtGui.QPainter()
        painter.begin(self.pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        text = "{} GHz".format(value)

        painter.setFont(QtGui.QFont('Tahoma', 30))
        painter.setPen(QtGui.QPen(QtGui.QColor('#e0e0e0')))
        painter.drawText(self.get_relative_width(25.5),
                         self.get_relative_height(68), text)

        painter.setFont(QtGui.QFont('Tahoma', 30))
        painter.setPen(QtGui.QPen(QtGui.QColor('#000000')))
        painter.drawText(self.get_relative_width(25),
                         self.get_relative_height(70), text)

        text = "CPU frequency"

        painter.setFont(QtGui.QFont('Tahoma', 15))
        painter.setPen(QtGui.QPen(QtGui.QColor('#e0e0e0')))
        painter.drawText(self.get_relative_width(25.5),
                         self.get_relative_height(78), text)

        painter.setFont(QtGui.QFont('Tahoma', 15))
        painter.setPen(QtGui.QPen(QtGui.QColor('#000000')))
        painter.drawText(self.get_relative_width(25),
                         self.get_relative_height(80), text)

        painter.end()

        return self.pixmap


class StatisticPainterCPUFrequencyChart(StatisticPainterAbstract):
    def __init__(self, pixmap):
        super(StatisticPainterCPUFrequencyChart, self).__init__(pixmap)
        self.points = []

    def append(self, point):
        if len(self.points) >= self.width / 31:
            self.points.pop(0)
        self.points.append(point)

    def refresh(self, value):
        if float(value) <= 0:
            return self.pixmap

        value = (float(value) / 100 * self.height) / 1.5
        self.append(value if value <= self.height else self.height)

        painter = QtGui.QPainter()
        painter.begin(self.pixmap)

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        for index, point in enumerate(self.points, start=1):
            x = 30 * index + 4
            x = x - 15
            y = self.height - (self.height / 1.5) - 5
            painter.setPen(QtGui.QPen(QtGui.QColor('#f0f0f0'), 28))
            painter.drawLine(x, y, x, self.height)

            x = 30 * index + 2
            x = x - 15
            y = self.height - point - 5
            painter.setPen(QtGui.QPen(QtGui.QColor('#e0e0e0'), 28))
            painter.drawLine(x, y, x, self.height)

            x = 30 * index
            x = x - 15
            y = self.height - point
            painter.setPen(QtGui.QPen(QtCore.Qt.green, 28))
            painter.drawLine(x, y, x, self.height)

        painter.end()

        return self.pixmap


class StatisticPainterGitter(StatisticPainterAbstract):
    def __init__(self, pixmap):
        super(StatisticPainterGitter, self).__init__(pixmap)
        self.points = []

    def refresh(self, value):
        painter = QtGui.QPainter()
        painter.begin(self.pixmap)

        pen = QtGui.QPen(QtGui.QColor('#f4f4f4'))
        pen.setWidth(1)
        painter.setPen(pen)

        painter.setRenderHint(QtGui.QPainter.Antialiasing, True)
        for position in range(0, self.width, int(self.width / 30)):
            painter.drawLine(position, 0, position, self.height)

        for position in range(0, self.height, int(self.height / 20)):
            painter.drawLine(0, position, self.width, position)

        painter.end()

        return self.pixmap


class StatisticPainterBackground(StatisticPainterAbstract):
    def __init__(self, pixmap):
        super(StatisticPainterBackground, self).__init__(pixmap)
        self.points = []

    def refresh(self, value):
        self.pixmap.fill(Qt.white)
        return self.pixmap
