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
<h2>nmi_watchdog</h2>
<p>This parameter can be used to control the NMI watchdog(i.e. the hard lockup detector) on x86 systems.</p>
<p><b>0</b> - disable the hard lockup detector</p>
<p><b>1</b> - enable the hard lockup detector</p>

<p>The hard lockup detector monitors each CPU for its ability to respond totimer interrupts. The mechanism utilizes CPU performance counter registers
that are programmed to generate Non-Maskable Interrupts (NMIs) periodicallywhile a CPU is busy. Hence, the alternative name 'NMI watchdog'.</p>

<p>The NMI watchdog is disabled by default if the kernel is running as a guest in a KVM virtual machine. This default can be overridden by adding</p>
<p><b>nmi_watchdog=1</b></p>
"""
