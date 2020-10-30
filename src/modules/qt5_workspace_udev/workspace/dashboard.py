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
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class DashboardWidget(QtWidgets.QSplitter):

    @inject.params(performance='udev_rules.performance', powersave='udev_rules.powersave')
    def __init__(self, performance, powersave):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.left = QtWidgets.QTextEdit()
        self.right = QtWidgets.QTextEdit()

        self.addWidget(self.left)
        self.addWidget(self.right)

        self.setCollapsible(0, False)
        self.setCollapsible(1, False)

        performance_text = []
        for rule in performance.rules:
            performance_text.append(rule)
        self.setTextLeft("\n".join(performance_text))

        powersave_text = []
        for rule in powersave.rules:
            powersave_text.append(rule)
        self.setTextRight("\n".join(powersave_text))

    def setTextLeft(self, text):
        self.left.setText(text)

    def setTextRight(self, text):
        self.right.setText(text)
