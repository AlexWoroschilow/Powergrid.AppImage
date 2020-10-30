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
from string import Template

import inject

from .gui.settings.settings import DashboardSettingsPerformance
from .gui.settings.settings import DashboardSettingsPowersave
from .service import Finder


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

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

    @inject.params(config='config')
    def _performance(self, config=None):
        with open('templates/writeback.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/performance_writeback', template.substitute(
                schema=config.get('writeback.performance', ''),
                ignored="'{}'".format("','".join(self._ignores(1)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _powersave(self, config=None):
        with open('templates/writeback.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/powersave_writeback', template.substitute(
                schema=config.get('writeback.powersave', '1500'),
                ignored="'{}'".format("','".join(self._ignores(2)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _cleanup(self, config=None):
        return ('/etc/performance-tuner/performance_writeback',
                '/etc/performance-tuner/powersave_writeback')

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):

        storage.dispatch({
            'type': '@@app/exporter/performance/writeback',
            'action': self._performance
        })

        storage.dispatch({
            'type': '@@app/exporter/powersave/writeback',
            'action': self._powersave
        })

        storage.dispatch({
            'type': '@@app/exporter/cleanup/writeback',
            'action': self._cleanup
        })


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    binder.bind_to_constructor('plugin.service.writeback', Finder)


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
    @inject.params(config='config', service='plugin.service.writeback')
    def rule_performance(config, service):
        for device in service.devices():
            if not os.path.exists(device.path):
                continue

            schema = config.get('writeback.performance', '')
            yield 'echo {} > /proc/sys/vm/dirty_writeback_centisecs'.format(schema)

    @powersave.rule()
    @inject.params(config='config', service='plugin.service.writeback')
    def rule_powersave(config, service):
        for device in service.devices():
            if not os.path.exists(device.path):
                continue

            schema = config.get('writeback.powersave', '1500')
            yield 'echo {} > /proc/sys/vm/dirty_writeback_centisecs'.format(schema)
