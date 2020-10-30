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
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


class DashboardDescription(QtWidgets.QLabel):

    def __init__(self):
        super(DashboardDescription, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.setAlignment(Qt.AlignTop)
        self.setText(self.description)
        self.setWordWrap(True)

    @property
    def description(self):
        return """
        <p>This file contains one of two words: <b>on</b> or <b>auto</b>. You can write those words to the file to change the device’s setting.</p>
        <p><b>on</b> means that the device should be resumed and autosuspend is not allowed. (Of course, system suspends are still allowed.)</p>
        <p><b>auto</b> is the normal state in which the kernel is allowed to autosuspend and autoresume the device.</p>
        """
