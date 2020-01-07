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
        self.setText(self.description)
        self.setWordWrap(True)

    @property
    def description(self):
        return """
<h2>watchdog</h2>
<p>This parameter can be used to disable or enable the soft lockup detector and the NMI watchdog (i.e. the hard lockup detector) at the same time.</p>
<p><b>0</b> - disable the lockup detector</p>
<p><b>1</b> - enable the lockup detector</p>

<p>The <b>soft lockup detector</b> monitors CPUs for threads that are hogging the CPUs without rescheduling voluntarily, and thus prevent the 'watchdog/N' threads
from running. The mechanism depends on the CPUs ability to respond to timer interrupts which are needed for the 'watchdog/N' threads to be woken up by
the watchdog timer function, otherwise the NMI watchdog - if enabled - can detect a hard lockup condition.</p>

<p>The <b>hard lockup detector</b> monitors each CPU for its ability to respond to timer interrupts. The mechanism utilizes CPU performance counter registers
that are programmed to generate Non-Maskable Interrupts (NMIs) periodicallywhile a CPU is busy. Hence, the alternative name 'NMI watchdog'.</p>

<p>The soft lockup detector and the NMI watchdog can also be disabled or enabled individually, using the soft_watchdog and nmi_watchdog parameters.</p>
"""
