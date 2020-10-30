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
<p>Performance Tuner is a free open source program for the energy consumption fine-tuning in Linux.</p>
<p>The graphical interface allows you to configure and generate scripts which will be executed in the background by triggers from qt5_workspace_udev.</p>
""")


class DashboardDescriptionDeviceManagement(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionDeviceManagement, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("""<p>Using these settings, you can force the power-saving or performance mode to be enabled.</p>
<p>Please note that according to the architecture of the program, the selected power-mode will be applied at the moment of switching of the power supply. 
The selected mode <b>will not be turned on immediately</b>, but the device will be <b>ignored when switching</b> to the opposite mode.</p>
""")


class DashboardDescriptionACAdapter(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionACAdapter, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("""<p>These settings will be applied when powered from the AC-Adapter. Settings will be applied only 
once during the switch of the power source. After that, you can change the settings <b>manually</b> or with the help of the <b>powertop</b>. 
These changes will work until the next switching of the power supply</p>""")


class DashboardDescriptionBattery(DashboardDescription):

    def __init__(self):
        super(DashboardDescriptionBattery, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("""<p>These settings will be applied when powered from the Battery. Settings will be applied only 
once during the switch of the power source. After that, you can change the settings <b>manually</b> or with the help of the <b>powertop</b>. 
These changes will work until the next switching of the power supply</p>""")


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
