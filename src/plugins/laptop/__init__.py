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
import functools
from string import Template

from .service import Finder
from .gui.settings.settings import DashboardSettingsPerformance
from .gui.settings.settings import DashboardSettingsPowersave


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config', service='plugin.service.laptop')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []
        for device in service.devices():
            value_ignored = config.get('laptop.permanent.{}'.format(device.name), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored

    @inject.params(config='config')
    def _performance(self, config=None):
        with open('templates/laptop.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/performance_laptop', template.substitute(
                schema=config.get('laptop.performance', '0'),
                ignored="'{}'".format("','".join(self._ignores(1)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _powersave(self, config=None):
        with open('templates/laptop.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/powersave_laptop', template.substitute(
                schema=config.get('laptop.powersave', '5'),
                ignored="'{}'".format("','".join(self._ignores(2)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _cleanup(self, config=None):
        return ('/etc/performance-tuner/performance_laptop',
                '/etc/performance-tuner/powersave_laptop')

    @property
    def enabled(self):
        return os.path.exists('/proc/sys/vm/laptop_mode')

    def configure(self, binder, options, args):
        binder.bind_to_constructor('plugin.service.laptop', functools.partial(
            Finder, path='/proc/sys/vm/laptop_mode'
        ))

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):

        storage.dispatch({
            'type': '@@app/dashboard/settings/performance/laptop',
            'action': DashboardSettingsPerformance,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/dashboard/settings/powersave/laptop',
            'action': DashboardSettingsPowersave,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/exporter/performance/laptop',
            'action': self._performance
        })

        storage.dispatch({
            'type': '@@app/exporter/powersave/laptop',
            'action': self._powersave
        })

        storage.dispatch({
            'type': '@@app/exporter/cleanup/laptop',
            'action': self._cleanup
        })


module = Loader()
