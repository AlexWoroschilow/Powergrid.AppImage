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


class DashboardSettingsPerformance(QtWidgets.QWidget):

    @inject.params(storage='storage')
    def __init__(self, storage=None):
        super(DashboardSettingsPerformance, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)

        state = storage.get_state()
        if state is None: return None

        widget = QtWidgets.QWidget()
        widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        widget.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(widget)

        for bundle in sorted(state.settings.performance, key=lambda x: x[1]):
            constructor, priority = bundle
            if not callable(constructor):
                continue

            child = constructor()
            if child is None: continue

            widget.layout().addWidget(child)


class DashboardSettingsPowersave(QtWidgets.QWidget):

    @inject.params(storage='storage')
    def __init__(self, storage=None):
        super(DashboardSettingsPowersave, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)

        state = storage.get_state()
        if state is None: return None

        widget = QtWidgets.QWidget()
        widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        widget.setLayout(QtWidgets.QHBoxLayout())
        self.layout().addWidget(widget)

        for bundle in sorted(state.settings.powersave, key=lambda x: x[1]):
            constructor, priority = bundle
            if not callable(constructor):
                continue

            child = constructor()
            if child is None: continue

            widget.layout().addWidget(child)


class DashboardSettingsDevices(QtWidgets.QWidget):

    @inject.params(storage='storage')
    def __init__(self, storage=None):
        super(DashboardSettingsDevices, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setContentsMargins(0, 0, 0, 0)

        state = storage.get_state()
        if state is None: return None

        for bundle in sorted(state.devices, key=lambda x: x[1]):
            constructor, priority = bundle
            if not callable(constructor):
                continue

            widget = constructor()
            if widget is None: continue

            self.layout().addWidget(widget)
