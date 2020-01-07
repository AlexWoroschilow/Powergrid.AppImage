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
<p>To increase the effectiveness of the laptop_mode strategy, the laptop_mode
control script increases dirty_expire_centisecs and <b>dirty_writeback_centisecs</b> in
<b>/proc/sys/vm</b> to about <b>10</b> minutes (by default), which means that pages that are
dirtied are not forced to be written to disk as often.</p>
<p>The control script also changes the dirty background ratio, so that background writeback of dirty pages
is not done anymore. Combined with a higher commit value (also 10 minutes) for
ext3 or ReiserFS filesystems (also done automatically by the control script),
this results in concentration of disk activity in a small time interval which
occurs only once every <b>10</b> minutes, or whenever the disk is forced to spin up by
a cache miss. The disk can then be spun down in the periods of inactivity.</p>
"""
