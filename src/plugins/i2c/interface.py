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
import os

import hexdi

from modules import qt5_window
from modules import qt5_workspace_adapter
from modules import qt5_workspace_battery
from modules.qt5_workspace_udev import performance
from modules.qt5_workspace_udev import powersave

config = hexdi.resolve('config')
config.set('default.performance.i2c', 'on')
config.set('default.powersave.i2c', 'auto')


@qt5_window.workspace(name='I2C', focus=False, position=6)
@hexdi.inject('workspace.i2c')
def window_workspace(parent, workspace):
    return workspace


@qt5_workspace_battery.element()
def battery_element(parent=None):
    from .settings.panel import SettingsPowersaveWidget
    return SettingsPowersaveWidget()


@qt5_workspace_adapter.element()
def adapter_element(parent=None):
    from .settings.panel import SettingsPerformanceWidget
    return SettingsPerformanceWidget()


@performance.rule()
@hexdi.inject('config', 'plugin.service.i2c')
def rule_performance(config, service):
    for device in service.devices():
        permanent = config.get('i2c.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path):
            continue

        schema = config.get('default.performance.i2c')
        schema = config.get('i2c.performance', schema)
        schema = config.get('default.powersave.i2c') if int(permanent) == 1 else schema
        schema = config.get('default.performance.i2c') if int(permanent) == 2 else schema

        file = '{}/power/control'.format(device.path)
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.i2c')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('i2c.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path):
            continue

        schema = config.get('default.powersave.i2c')
        schema = config.get('i2c.powersave', schema)
        schema = config.get('default.powersave.i2c') if int(permanent) == 1 else schema
        schema = config.get('default.performance.i2c') if int(permanent) == 2 else schema

        file = '{}/power/control'.format(device.path)
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
