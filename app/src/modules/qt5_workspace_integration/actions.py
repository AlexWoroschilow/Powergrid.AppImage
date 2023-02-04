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


@hexdi.inject('udev_dumper.schema', 'window.dialog_manager')
def onActonApply(event, schema, dialog_manager):
    single_shot = schema.dump(os.path.expanduser('/tmp/performance/schema.sh'))
    if dialog_manager.execute(single_shot) == QtWidgets.QMessageBox.Cancel:
        return shutil.rmtree(os.path.dirname(single_shot))

    try:
        os.system('pkexec sh {} '.format(single_shot))
        return shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
    except Exception as ex:
        shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
        return dialog_manager.error("{}".format(ex))

    return self


@hexdi.inject('udev_dumper.cleaner', 'window.dialog_manager')
def onActionCleanup(event, dumper, dialog_manager):
    single_shot = dumper.dump(os.path.expanduser('/tmp/performance/cleaner.sh'))
    if dialog_manager.execute(single_shot) == QtWidgets.QMessageBox.Cancel:
        return shutil.rmtree(os.path.dirname(single_shot))

    try:
        os.system('pkexec sh {} '.format(single_shot))
        return shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
    except Exception as ex:
        shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
        return dialog_manager.error("{}".format(ex))


@hexdi.inject('udev_dumper.performance', 'window.dialog_manager')
def onActionPerformace(event, dumper, dialog_manager):
    single_shot = dumper.dump(os.path.expanduser('/tmp/performance/performance.sh'))
    if dialog_manager.execute(single_shot) == QtWidgets.QMessageBox.Cancel:
        return shutil.rmtree(os.path.dirname(single_shot))

    try:
        os.system('pkexec sh {} '.format(single_shot))
        return shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
    except Exception as ex:
        shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
        return dialog_manager.error("{}".format(ex))


@hexdi.inject('udev_dumper.powersave', 'window.dialog_manager')
def onActionPowerSave(event, dumper, dialog_manager):
    single_shot = dumper.dump(os.path.expanduser('/tmp/performance/powersave.sh'))
    if dialog_manager.execute(single_shot) == QtWidgets.QMessageBox.Cancel:
        return shutil.rmtree(os.path.dirname(single_shot))

    try:
        os.system('pkexec sh {} '.format(single_shot))
        return shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
    except Exception as ex:
        shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
        return dialog_manager.error("{}".format(ex))
