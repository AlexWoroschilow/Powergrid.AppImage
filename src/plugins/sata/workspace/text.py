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
<p>Tell the controller to try to make the link use the least possible power when possible.  This may sacrifice some performance due to increased latency when coming out of lower power states.</p>
<p>Tell the controller to enter a lower power state when possible, but do not enter the lowest power state, thus improving latency over min_power setting.</p>
<p>Generally, this means no power management.  Tell the controller to have performance be a priority over power management.</p>
"""
