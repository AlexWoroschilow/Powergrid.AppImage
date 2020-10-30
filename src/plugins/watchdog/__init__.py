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

from .gui.settings.settings import DashboardSettingsPerformance
from .gui.settings.settings import DashboardSettingsPowersave
from .service import Finder


class Loader(object):

    @inject.params(config='config', service='plugin.service.watchdog')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []

        for device in service.devices():
            value_ignored = config.get('watchdog.permanent.{}'.format(device.name), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    binder.bind_to_constructor('plugin.service.watchdog', Finder)


def bootstrap(options: {} = None, args: [] = None):
    from modules import qt5_workspace_battery
    from modules import qt5_workspace_adapter

    @qt5_workspace_battery.element()
    def battery_element(parent=None):
        return DashboardSettingsPowersave()

    @qt5_workspace_adapter.element()
    def adapter_element(parent=None):
        return DashboardSettingsPerformance()

    from modules.qt5_workspace_udev import performance
    from modules.qt5_workspace_udev import powersave

    @performance.rule()
    @inject.params(config='config', service='plugin.service.watchdog')
    def rule_performance(config, service):
        for device in service.devices():
            if not os.path.exists(device.path):
                continue

            schema = config.get('watchdog.performance', '1')
            yield 'echo {} > {}'.format(schema, device.path)

    @powersave.rule()
    @inject.params(config='config', service='plugin.service.watchdog')
    def rule_powersave(config, service):
        for device in service.devices():
            if not os.path.exists(device.path):
                continue

            schema = config.get('watchdog.powersave', '0')
            yield 'echo {} > {}'.format(schema, device.path)
