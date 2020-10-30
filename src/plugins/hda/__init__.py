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


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    """

    :param binder:
    :param options:
    :param args:
    :return:
    """
    from .service import Finder
    binder.bind_to_constructor('plugin.service.hda', Finder)

    from .workspace.settings import SettingsWidget
    binder.bind_to_constructor('workspace.hda', SettingsWidget)


def bootstrap(options: {} = None, args: [] = None):
    """

    :param options:
    :param args:
    :return:
    """
    from modules import qt5_window
    from modules import qt5_workspace_battery
    from modules import qt5_workspace_adapter
    from modules.qt5_workspace_udev import performance
    from modules.qt5_workspace_udev import powersave

    @qt5_window.workspace(name='Intel HDA', focus=False, position=3)
    @inject.params(workspace='workspace.hda')
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

    @performance.rule()
    @inject.params(config='config', service='plugin.service.hda')
    def rule_performance(config, service):
        for device in service.devices():
            permanent = config.get('hda.permanent.{}'.format(device.code), 0)
            if not os.path.exists(device.path):
                continue

            file = '{}/parameters/power_save'.format(device.path)
            schema = config.get('hda.performance', '')
            schema = '5' if int(permanent) == 1 else schema
            schema = '' if int(permanent) == 2 else schema
            if os.path.exists(file) and os.path.isfile(file):
                yield 'ls {} && echo {} > {}'.format(device.path, schema, file)

    @powersave.rule()
    @inject.params(config='config', service='plugin.service.hda')
    def rule_powersave(config, service):
        for device in service.devices():
            permanent = config.get('hda.permanent.{}'.format(device.code), 0)
            if not os.path.exists(device.path):
                continue

            file = '{}/parameters/power_save'.format(device.path)
            schema = config.get('hda.powersave', '5')
            schema = '5' if int(permanent) == 1 else schema
            schema = '' if int(permanent) == 2 else schema
            if os.path.exists(file) and os.path.isfile(file):
                yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
