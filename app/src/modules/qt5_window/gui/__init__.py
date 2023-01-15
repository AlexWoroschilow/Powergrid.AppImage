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
from PyQt5 import QtCore
from PyQt5 import QtWidgets

import functools

from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class ToolBarButton(QtWidgets.QPushButton):
    activate = QtCore.pyqtSignal(object)

    def __init__(self, name=None):
        super(ToolBarButton, self).__init__(name)
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)

        self.setFlat(True)

    def connected(self):
        try:
            receiversCount = self.receivers(self.clicked)
            return receiversCount > 0
        except (SyntaxError, RuntimeError) as err:
            return False
