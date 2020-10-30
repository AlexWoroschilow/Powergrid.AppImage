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

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config', service='plugin.service.usb')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []
        for device in service.devices():
            value_ignored = config.get('usb.permanent.{}'.format(device.code), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    from .workspace.settings import SettingsWidget
    binder.bind_to_constructor('workspace.usb', SettingsWidget)
    binder.bind_to_constructor('plugin.service.usb', Finder)


def bootstrap(options: {} = None, args: [] = None):
    from modules import qt5_window
    from modules import qt5_workspace_battery
    from modules import qt5_workspace_adapter
    from modules.qt5_workspace_udev import performance
    from modules.qt5_workspace_udev import powersave

    @qt5_window.workspace(name='USB', focus=False, position=2)
    @inject.params(workspace='workspace.usb')
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
    @inject.params(config='config', service='plugin.service.usb')
    def rule_performance(config, service):
        for device in service.devices():
            if not os.path.exists(device.path):
                continue

            file = '{}/power/level'.format(device.path)
            schema = config.get('usb.performance.power_level', 'on')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

            file = '{}/power/control'.format(device.path)
            schema = config.get('usb.performance.power_control', 'on')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

            file = '{}/power/autosuspend'.format(device.path)
            schema = config.get('usb.performance.autosuspend', '-1')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

            file = '{}/power/autosuspend_delay_ms'.format(device.path)
            schema = config.get('usb.performance.autosuspend_delay', '-1')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

    @powersave.rule()
    @inject.params(config='config', service='plugin.service.usb')
    def rule_powersave(config, service):
        for device in service.devices():
            if not os.path.exists(device.path):
                continue

            file = '{}/power/level'.format(device.path)
            schema = config.get('usb.powersave.power_level', 'auto')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

            file = '{}/power/control'.format(device.path)
            schema = config.get('usb.powersave.power_control', 'auto')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

            file = '{}/power/autosuspend'.format(device.path)
            schema = config.get('usb.powersave.autosuspend', '500')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)

            file = '{}/power/autosuspend_delay_ms'.format(device.path)
            schema = config.get('usb.powersave.autosuspend_delay', '500')
            if os.path.exists(file) and os.path.isfile(file):
                yield 'echo {} > {}'.format(schema, file)
