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

from modules import qt5_workspace_adapter
from modules import qt5_workspace_battery
from modules.qt5_workspace_udev import performance
from modules.qt5_workspace_udev import powersave
from .gui.settings.settings import DashboardSettingsPerformance
from .gui.settings.settings import DashboardSettingsPowersave

config = hexdi.resolve('config')
config.set('default.performance.watchdog', 1)
config.set('default.powersave.watchdog', 0)


@qt5_workspace_battery.element()
def battery_element(parent):
    return DashboardSettingsPowersave()


@qt5_workspace_adapter.element()
def adapter_element(parent):
    return DashboardSettingsPerformance()


@performance.rule()
@hexdi.inject('config', 'plugin.service.watchdog')
def rule_performance(config, service):
    for device in service.devices():
        permanent = config.get('watchdog.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        schema = config.get('default.performance.watchdog')
        schema = config.get('watchdog.performance', schema)
        schema = config.get('default.performance.watchdog') if int(permanent) == 1 else schema
        schema = config.get('default.powersave.watchdog') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, device.path)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.watchdog')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('watchdog.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        schema = config.get('default.powersave.watchdog')
        schema = config.get('watchdog.powersave', schema)
        schema = config.get('default.performance.watchdog') if int(permanent) == 1 else schema
        schema = config.get('default.powersave.watchdog') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, device.path)
