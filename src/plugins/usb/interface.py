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
from .settings.panel import SettingsPerformanceWidget
from .settings.panel import SettingsPowersaveWidget

config = hexdi.resolve('config')
config.set('default.performance.usb', 'on')
config.set('default.performance.usb.power_level', 'on')
config.set('default.performance.usb.power_control', 'on')
config.set('default.performance.usb.autosuspend_delay', -1)
config.set('default.performance.usb.autosuspend', -1)

config.set('default.powersave.usb', 'auto')
config.set('default.powersave.usb.power_level', 'auto')
config.set('default.powersave.usb.power_control', 'auto')
config.set('default.powersave.usb.autosuspend_delay', 500)
config.set('default.powersave.usb.autosuspend', 500)


@qt5_window.workspace(name='USB', focus=False, position=2)
@hexdi.inject('workspace.usb')
def window_workspace(parent, workspace):
    return workspace


@qt5_workspace_battery.element()
def battery_element(parent):
    return SettingsPowersaveWidget()


@qt5_workspace_adapter.element()
def adapter_element(parent):
    return SettingsPerformanceWidget()


@performance.rule()
@hexdi.inject('config', 'plugin.service.usb')
def rule_performance(config, service):
    for device in service.devices():
        permanent = config.get('usb.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/power/level'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.performance.usb.power_level')
            schema = config.get('usb.performance.power_level', schema)
            schema = config.get('default.powersave.usb.power_level') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.power_level') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/control'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.performance.usb.power_control')
            schema = config.get('usb.performance.power_control', schema)
            schema = config.get('default.powersave.usb.power_control') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.power_control') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.performance.usb.autosuspend')
            schema = config.get('usb.performance.autosuspend', schema)
            schema = config.get('default.powersave.usb.autosuspend') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.autosuspend') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend_delay_ms'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.performance.usb.autosuspend_delay')
            schema = config.get('usb.performance.autosuspend_delay', schema)
            schema = config.get('default.powersave.usb.autosuspend_delay') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.autosuspend_delay') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.usb')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('usb.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/power/level'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.powersave.usb.power_level')
            schema = config.get('usb.powersave.power_level', schema)
            schema = config.get('default.powersave.usb.power_level') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.power_level') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/control'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.powersave.usb.power_control')
            schema = config.get('usb.powersave.power_control', schema)
            schema = config.get('default.powersave.usb.power_control') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.power_control') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.powersave.usb.autosuspend')
            schema = config.get('usb.powersave.autosuspend', schema)
            schema = config.get('default.powersave.usb.autosuspend') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.autosuspend') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend_delay_ms'.format(device.path)
        if os.path.exists(file) and os.path.isfile(file):
            schema = config.get('default.powersave.usb.autosuspend_delay')
            schema = config.get('usb.powersave.autosuspend_delay', schema)
            schema = config.get('default.powersave.usb.autosuspend_delay') if int(permanent) == 1 else schema
            schema = config.get('default.performance.usb.autosuspend_delay') if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
