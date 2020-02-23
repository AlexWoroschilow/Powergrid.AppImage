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
import inject
import functools
from string import Template

from .gui.settings.settings import DashboardSettingsPerformance
from .gui.settings.settings import DashboardSettingsPowersave
from .gui.devices.properties import DashboardProperties


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        """
        Setup plugin services

        :param binder:
        :param options:
        :param args:
        :return:
        """
        from .service import Finder

        binder.bind_to_constructor('plugin.service.cpu', functools.partial(
            Finder, path='/sys/devices/system/cpu'
        ))

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):
        """
        Define the services and setup the service-container
        :param options:
        :param args:
        :param storage:
        :return:
        """

        storage.dispatch({
            'type': '@@app/dashboard/settings/performance/cpu',
            'action': DashboardSettingsPerformance,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/dashboard/settings/powersave/cpu',
            'action': DashboardSettingsPowersave,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/dashboard/properties/cpu',
            'action': DashboardProperties,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/exporter/performance/cpu',
            'action': self._performance
        })

        storage.dispatch({
            'type': '@@app/exporter/powersave/cpu',
            'action': self._powersave
        })

        storage.dispatch({
            'type': '@@app/exporter/cleanup/cpu',
            'action': self._cleanup
        })

    @inject.params(config='config', service='plugin.service.cpu')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []
        for device in service.cores():
            value_ignored = config.get('cpu.permanent.{}'.format(device.code), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored

    @inject.params(config='config')
    def _performance(self, config=None):

        with open('templates/cpu.tpl', 'r') as stream:
            template = Template(stream.read())

            return ('/etc/performance-tuner/performance_cpu', template.substitute(
                schema=config.get('cpu.performance', 'ondemand'),
                ignored="'{}'".format("','".join(self._ignores(1)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _powersave(self, config=None):

        with open('templates/cpu.tpl', 'r') as stream:
            template = Template(stream.read())

            return ('/etc/performance-tuner/powersave_cpu', template.substitute(
                schema=config.get('cpu.powersave', 'powersave'),
                ignored="'{}'".format("','".join(self._ignores(2)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _cleanup(self, config=None):
        return ('/etc/performance-tuner/performance_cpu',
                '/etc/performance-tuner/powersave_cpu')


module = Loader()
