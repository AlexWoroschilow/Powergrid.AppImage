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
import os

import hexdi

from modules import qt5_window
from modules import qt5_workspace_adapter
from modules import qt5_workspace_battery
from modules.qt5_workspace_udev import performance
from modules.qt5_workspace_udev import powersave
from .settings.panel import SettingsPerformanceWidget
from .settings.panel import SettingsPowersaveWidget


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
        if not os.path.exists(device.path):
            continue

        file = '{}/power/level'.format(device.path)
        schema = config.get('usb.performance.power_level', 'on')
        schema = 'auto' if int(permanent) == 1 else schema
        schema = 'on' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/control'.format(device.path)
        schema = config.get('usb.performance.power_control', 'on')
        schema = 'auto' if int(permanent) == 1 else schema
        schema = 'on' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend'.format(device.path)
        schema = config.get('usb.performance.autosuspend', '-1')
        schema = '500' if int(permanent) == 1 else schema
        schema = '-1' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend_delay_ms'.format(device.path)
        schema = config.get('usb.performance.autosuspend_delay', '-1')
        schema = '500' if int(permanent) == 1 else schema
        schema = '-1' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.usb')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('usb.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path):
            continue

        file = '{}/power/level'.format(device.path)
        schema = config.get('usb.powersave.power_level', 'auto')
        schema = 'auto' if int(permanent) == 1 else schema
        schema = 'on' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/control'.format(device.path)
        schema = config.get('usb.powersave.power_control', 'auto')
        schema = 'auto' if int(permanent) == 1 else schema
        schema = 'on' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend'.format(device.path)
        schema = config.get('usb.powersave.autosuspend', '500')
        schema = '500' if int(permanent) == 1 else schema
        schema = '-1' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

        file = '{}/power/autosuspend_delay_ms'.format(device.path)
        schema = config.get('usb.powersave.autosuspend_delay', '500')
        schema = '500' if int(permanent) == 1 else schema
        schema = '-1' if int(permanent) == 2 else schema
        if os.path.exists(file) and os.path.isfile(file):
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
