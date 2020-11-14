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
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

from .label import SettingsTitle
from .label import SettingsDescription


class WidgetSettingsAbout(QtWidgets.QWidget):

    def __init__(self):
        super(WidgetSettingsAbout, self).__init__()
        self.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)

        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setAlignment(Qt.AlignLeft)

        self.layout().addWidget(SettingsTitle('About performance tuner'))
        self.layout().addWidget(SettingsDescription("""<p>Performance Tuner is a free open source program 
for the energy consumption fine-tuning in Linux.</p>
<h5>Autor: Alex Woroschilow</h5>
<h5>Sources: https://github.com/AlexWoroschilow/AOD-PerformanceTuner</h5>
        """))
