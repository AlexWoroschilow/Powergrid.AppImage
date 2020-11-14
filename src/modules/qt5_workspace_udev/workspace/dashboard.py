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
import hexdi
from PyQt5 import QtCore
from PyQt5 import QtWidgets

from .label import TitleWidget


class DashboardWidget(QtWidgets.QSplitter):
    actionReload = QtCore.pyqtSignal(object)

    def __init__(self):
        super(DashboardWidget, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setContentsMargins(0, 0, 0, 0)

        self.left = QtWidgets.QTextEdit()
        self.right = QtWidgets.QTextEdit()

        self.container1 = QtWidgets.QWidget()
        self.container1.setLayout(QtWidgets.QVBoxLayout())
        self.container1.layout().setContentsMargins(0, 0, 0, 0)

        self.container1.layout().addWidget(TitleWidget('Performance rules'))
        self.container1.layout().addWidget(self.left)

        self.container2 = QtWidgets.QWidget()
        self.container2.setLayout(QtWidgets.QVBoxLayout())
        self.container2.layout().setContentsMargins(0, 0, 0, 0)
        self.container2.layout().addWidget(TitleWidget('Powersave rules'))
        self.container2.layout().addWidget(self.right)

        self.addWidget(self.container1)
        self.addWidget(self.container2)

        self.setCollapsible(0, False)
        self.setCollapsible(1, False)

        self.actionReload.connect(self.reloadEvent)

    @hexdi.inject('udev_rules.performance', 'udev_rules.powersave')
    def reloadEvent(self, event, performance, powersave):
        performance_text = []
        for rule in performance.rules:
            performance_text.append(rule)
        self.setTextLeft("\n".join(performance_text))

        powersave_text = []
        for rule in powersave.rules:
            powersave_text.append(rule)
        self.setTextRight("\n".join(powersave_text))

    def event(self, QEvent):
        if type(QEvent) == QtCore.QEvent:
            if QEvent.type() == QtCore.QEvent.ShowToParent:
                self.actionReload.emit(())
        return super(DashboardWidget, self).event(QEvent)

    def setTextLeft(self, text):
        self.left.setText(text)

    def setTextRight(self, text):
        self.right.setText(text)
