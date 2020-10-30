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

import inject

from .service import Finder


class Loader(object):

    @inject.params(config='config', service='plugin.service.sata')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []
        for device in service.devices():
            value_ignored = config.get('sata.permanent.{}'.format(device.code), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    from .workspace.settings import SettingsWidget
    binder.bind_to_constructor('workspace.scsi', SettingsWidget)
    binder.bind_to_constructor('plugin.service.sata', Finder)


def bootstrap(options: {} = None, args: [] = None):
    from modules import qt5_workspace_battery
    from modules import qt5_workspace_adapter

    from modules import qt5_window

    @qt5_window.workspace(name='SCSI', focus=False, position=5)
    @inject.params(workspace='workspace.scsi')
    def window_workspace(parent=None, workspace=None):
        return workspace

    @qt5_workspace_battery.element()
    def battery_element(parent=None):
        from .settings.panel import SettingsPowersaveWidget
        return SettingsPowersaveWidget()

    @qt5_workspace_adapter.element()
    def adapter_element(parent=None):
        from .settings.panel import SettingsPerformanceWidget
        return SettingsPerformanceWidget()

    from modules.qt5_workspace_udev import performance
    from modules.qt5_workspace_udev import powersave

    @performance.rule()
    @inject.params(config='config', service='plugin.service.sata')
    def rule_performance(config, service):
        for device in service.devices():
            permanent = config.get('sata.permanent.{}'.format(device.code), 0)
            if not os.path.exists(device.path):
                continue

            file = '{}/scsi_host/{}/link_power_management_policy'. \
                format(device.path, os.path.basename(device.path))
            if not os.path.exists(file):
                continue

            schema = config.get('sata.performance', 'max_performance')
            schema = 'min_power' if int(permanent) == 1 else schema
            schema = 'max_performance' if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

    @powersave.rule()
    @inject.params(config='config', service='plugin.service.sata')
    def rule_powersave(config, service):
        for device in service.devices():
            permanent = config.get('sata.permanent.{}'.format(device.code), 0)
            if not os.path.exists(device.path):
                continue

            file = '{}/scsi_host/{}/link_power_management_policy'. \
                format(device.path, os.path.basename(device.path))
            if not os.path.exists(file):
                continue

            schema = config.get('sata.powersave', 'min_power')
            schema = 'min_power' if int(permanent) == 1 else schema
            schema = 'max_performance' if int(permanent) == 2 else schema
            yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
