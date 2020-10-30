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


class Loader(object):

    @inject.params(config='config', service='plugin.service.writeback')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []
        for device in service.devices():
            value_ignored = config.get('writeback.permanent.{}'.format(device.code), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    """
    Configure global services
    :param binder:
    :param options:
    :param args:
    :return:
    """
    from .service import Finder
    binder.bind_to_constructor('plugin.service.writeback', Finder)


def bootstrap(options: {} = None, args: [] = None):
    """

    :param options:
    :param args:
    :return:
    """
    from modules import qt5_workspace_battery
    from modules import qt5_workspace_adapter
    from modules.qt5_workspace_udev import performance
    from modules.qt5_workspace_udev import powersave

    @qt5_workspace_battery.element()
    def battery_element(parent=None):
        from .gui.settings.settings import DashboardSettingsPowersave
        return DashboardSettingsPowersave()

    @qt5_workspace_adapter.element()
    def adapter_element(parent=None):
        from .gui.settings.settings import DashboardSettingsPerformance
        return DashboardSettingsPerformance()

    @performance.rule()
    @inject.params(config='config', service='plugin.service.writeback')
    def rule_performance(config, service):
        for device in service.devices():
            permanent = config.get('writeback.permanent.{}'.format(device.code), 0)
            if not os.path.exists(device.path):
                continue

            file = '/proc/sys/vm/dirty_writeback_centisecs'
            schema = config.get('writeback.performance', '')
            schema = '1500' if int(permanent) == 1 else schema
            schema = '' if int(permanent) == 2 else schema
            if os.path.exists(file) and os.path.isfile(file):
                yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

    @powersave.rule()
    @inject.params(config='config', service='plugin.service.writeback')
    def rule_powersave(config, service):
        for device in service.devices():
            permanent = config.get('writeback.permanent.{}'.format(device.code), 0)
            if not os.path.exists(device.path):
                continue

            file = '/proc/sys/vm/dirty_writeback_centisecs'
            schema = config.get('writeback.powersave', '1500')
            schema = '1500' if int(permanent) == 1 else schema
            schema = '' if int(permanent) == 2 else schema
            if os.path.exists(file) and os.path.isfile(file):
                yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
