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

config = hexdi.resolve('config')
config.set('default.performance.sata.policy', 'max_performance')
config.set('default.balanced.sata.policy', 'med_power_with_dipm')
config.set('default.powersave.sata.policy', 'min_power')
config.set('default.performance.sata.control', 'on')
config.set('default.powersave.sata.control', 'auto')


@qt5_window.workspace(name='SCSI', focus=False, position=5)
@hexdi.inject('workspace.scsi')
def window_workspace(parent, workspace):
    return workspace


@qt5_workspace_battery.element()
def battery_element(parent):
    return SettingsPowersaveWidget()


@qt5_workspace_adapter.element()
def adapter_element(parent):
    return SettingsPerformanceWidget()


@performance.rule()
@hexdi.inject('config', 'plugin.service.sata')
def rule_performance(config, service):
    for device in service.devices():
        permanent = config.get('sata.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/power/control'.format(device.path)
        if not os.path.exists(file): continue

        schema = config.get('default.performance.sata.control')
        schema = config.get('sata.performance.control', schema)
        schema = config.get('default.powersave.sata.control') if int(permanent) == 1 else schema
        schema = config.get('default.performance.sata.control') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

    for device in service.devices():
        permanent = config.get('sata.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/scsi_host/{}/link_power_management_policy'. \
            format(device.path, os.path.basename(device.path))
        if not os.path.exists(file): continue

        schema = config.get('default.performance.sata.control')
        schema = config.get('sata.performance.policy', schema)
        schema = config.get('default.powersave.sata.control') if int(permanent) == 1 else schema
        schema = config.get('default.performance.sata.control') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.sata')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('sata.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/power/control'.format(device.path)
        if not os.path.exists(file): continue

        schema = config.get('default.powersave.sata.control')
        schema = config.get('sata.powersave.control', schema)
        schema = config.get('default.powersave.sata.control') if int(permanent) == 1 else schema
        schema = config.get('default.performance.sata.control') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

    for device in service.devices():
        permanent = config.get('sata.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/scsi_host/{}/link_power_management_policy'. \
            format(device.path, os.path.basename(device.path))
        if not os.path.exists(file): continue

        schema = config.get('default.powersave.sata.control')
        schema = config.get('sata.powersave.policy', schema)
        schema = config.get('default.powersave.sata.control') if int(permanent) == 1 else schema
        schema = config.get('default.performance.sata.control') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
