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


@qt5_window.workspace(name='Disc', focus=False, position=5)
@hexdi.inject('workspace.disc')
def window_workspace(parent, workspace):
    return workspace


@qt5_workspace_battery.element()
def battery_element(parent):
    return SettingsPowersaveWidget()


@qt5_workspace_adapter.element()
def adapter_element(parent):
    return SettingsPerformanceWidget()


@performance.rule()
@hexdi.inject('config', 'plugin.service.disc')
def rule_performance(config, service):
    for device in service.devices():
        permanent = config.get('disc.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path):
            continue

        file = '{}/power/control'.format(device.path)
        if not os.path.exists(file): continue

        schema = config.get('disc.performance', 'on')
        schema = 'auto' if int(permanent) == 1 else schema
        schema = 'on' if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.disc')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('disc.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path):
            continue

        file = '{}/power/control'.format(device.path)
        if not os.path.exists(file):
            continue
        schema = config.get('disc.powersave', 'auto')
        schema = 'auto' if int(permanent) == 1 else schema
        schema = 'on' if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
