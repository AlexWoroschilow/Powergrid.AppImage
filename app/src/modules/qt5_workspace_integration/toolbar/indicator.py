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
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class ToolbarButtonIndicator(QtWidgets.QLabel):
    def __init__(self, icon1=None, icon2=None):
        super(ToolbarButtonIndicator, self).__init__()

        self.icon1 = QPixmap(icon1).scaledToWidth(60, QtCore.Qt.SmoothTransformation)
        self.icon2 = QPixmap(icon2).scaledToWidth(60, QtCore.Qt.SmoothTransformation)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.refresh)
        self.timer.start(500)

    def refresh(self) -> None:
        file_udevrules = "/etc/udev/rules.d/70-performance.rules"

        self.setPixmap(
            self.icon1 if not os.path.exists(file_udevrules)
            else self.icon2
        )

        self.setToolTip(
            "The udev rules are not integrated into the system"
            if not os.path.exists(file_udevrules) else
            "Udev rules werer successfuly integrated into the system"
        )
