# Copyright 2023 Alex Woroschilow (alex.woroschilow@gmail.com)
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
import os
import shutil

import hexdi
from PyQt5 import QtWidgets


@hexdi.inject('udev_dumper.export')
def onActionExport(event, dumper):
    selector = QtWidgets.QFileDialog()
    selector.setDirectory(os.path.expanduser('~'))
    selector.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

    if not selector.exec_(): return None

    for path in selector.selectedFiles():
        dumper.dump(path)


@hexdi.inject('udev_dumper.performance')
def onActionExportPerformace(event, dumper):
    selector = QtWidgets.QFileDialog()
    selector.setDirectory(os.path.expanduser('~'))
    selector.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

    if not selector.exec_(): return None

    for path in selector.selectedFiles():
        dumper.dump(path)


@hexdi.inject('udev_dumper.powersave')
def onActionExportPowerSave(event, dumper):
    selector = QtWidgets.QFileDialog()
    selector.setDirectory(os.path.expanduser('~'))
    selector.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)

    if not selector.exec_(): return None

    for path in selector.selectedFiles():
        dumper.dump(path)
