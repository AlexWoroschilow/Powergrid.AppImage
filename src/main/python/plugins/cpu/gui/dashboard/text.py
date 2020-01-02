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
<h2>Performance</h2>
<p>When attached to a policy object, this governor causes the highest frequency, within the scaling_max_freq policy limit, to be requested for that policy.</p>
<p>The request is made once at that time the governor for the policy is set to performance and whenever the scaling_max_freq or scaling_min_freq policy limits change after that.</p></p>

<h2>Ondemand</h2>
<p>This governor uses CPU load as a CPU frequency selection metric.</p>
<p>In order to estimate the current CPU load, it measures the time elapsed between consecutive invocations of its worker routine and computes the fraction of that time in which the given CPU was not idle. The ratio of the non-idle (active) time to the total CPU time is taken as an estimate of the load.</p>
<p>If this governor is attached to a policy shared by multiple CPUs, the load is estimated for all of them and the greatest result is taken as the load estimate for the entire policy.</p>

<h2>Conservative</h2>
<p>This governor uses CPU load as a CPU frequency selection metric.</p>
<p>It estimates the CPU load in the same way as the ondemand governor described above, but the CPU frequency selection algorithm implemented by it is different.</p>
<p>Namely, it avoids changing the frequency significantly over short time intervals which may not be suitable for systems with limited power supply capacity (e.g. battery-powered). To achieve that, it changes the frequency in relatively small steps, one step at a time, up or down - depending on whether or not a (configurable) threshold has been exceeded by the estimated CPU load.</p>

<h2>Powersave</h2>
<p>When attached to a policy object, this governor causes the lowest frequency, within the scaling_min_freq policy limit, to be requested for that policy.</p>
<p>The request is made once at that time the governor for the policy is set to powersave and whenever the scaling_max_freq or scaling_min_freq policy limits change after that.</p>
"""
