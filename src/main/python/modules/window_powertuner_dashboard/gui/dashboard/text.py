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
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets


class DashboardDescription(QtWidgets.QLabel):

    def __init__(self):
        super(DashboardDescription, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("""
<p>Performance Tuner is a free open source program for the fine-tuning of the energy saving in Linux.</p>
<p>The graphical interface allows you to configure and generate scripts which will be executed in the background by triggers from udev.</p>
""")


class DashboardDescriptionACAdapter(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionACAdapter, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("""
<p><b>CPU</b> - frequencies can be scaled automatically depending on the system load, in response to ACPI events, or manually by userspace programs.</p>
<h3>HDA</h3>
<p></p>
<h3>I2C</h3>
<p></p>
<h3>Laptop</h3>
<p></p>
<h3>PCI</h3>
<p></p>
<h3>SATA</h3>
<p></p>
<h3>USB</h3>
<p></p>
<h3>Watchdog</h3>
<p></p>
<h3>Writeback</h3>
<p></p>
""")


class DashboardDescriptionBattery(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionBattery, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("""
<h3>CPU<h3>
<p></p>
<h3>HDA<h3>
<p></p>
<h3>I2C<h3>
<p></p>
<h3>Laptop<h3>
<p></p>
<h3>PCI<h3>
<p></p>
<h3>SATA<h3>
<p></p>
<h3>USB<h3>
<p></p>
<h3>Watchdog<h3>
<p></p>
<h3>Writeback<h3>
<p></p>        
""")


class DashboardDescriptionPerformance(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionPerformance, self).__init__()

    @property
    def description(self):
        return """
<p>When attached to a policy object, this governor causes the highest frequency, within the scaling_max_freq policy limit, to be requested for that policy.</p>
<p>The request is made once at that time the governor for the policy is set to performance and whenever the scaling_max_freq or scaling_min_freq policy limits change after that.</p></p>
"""


class DashboardDescriptionPowersave(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionPowersave, self).__init__()

    @property
    def description(self):
        return """
<p>When attached to a policy object, this governor causes the highest frequency, within the scaling_max_freq policy limit, to be requested for that policy.</p>
<p>The request is made once at that time the governor for the policy is set to performance and whenever the scaling_max_freq or scaling_min_freq policy limits change after that.</p></p>
"""
