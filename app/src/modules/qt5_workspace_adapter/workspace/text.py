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


class DescriptionWidget(QtWidgets.QLabel):

    def __init__(self):
        super(DescriptionWidget, self).__init__()
        self.setAlignment(Qt.AlignTop)
        self.setWordWrap(True)
        self.setText("The settings will only take effect when the device is being powered by the AC adapter "
                     "and will only be implemented once upon switching the power source.")
