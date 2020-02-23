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

from .service import Finder
from .gui.settings.settings import DashboardSettingsPerformance
from .gui.settings.settings import DashboardSettingsPowersave
from .gui.devices.properties import DashboardProperties


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

    @inject.params(config='config')
    def _performance(self, config=None):
        with open('templates/usb.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/performance_usb', template.substitute(
                power_level=config.get('usb.performance.power_level', 'on'),
                power_control=config.get('usb.performance.power_control', 'on'),
                autosuspend_delay=config.get('usb.performance.autosuspend_delay', '-1'),
                autosuspend=config.get('usb.performance.autosuspend', '-1'),
                ignored="'{}'".format("','".join(self._ignores(1)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _powersave(self, config=None):
        with open('templates/usb.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/powersave_usb', template.substitute(
                power_level=config.get('usb.powersave.power_level', 'auto'),
                power_control=config.get('usb.powersave.power_control', 'auto'),
                autosuspend_delay=config.get('usb.powersave.autosuspend_delay', '500'),
                autosuspend=config.get('usb.powersave.autosuspend', '500'),
                ignored="'{}'".format("','".join(self._ignores(2)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _cleanup(self, config=None):
        return ('/etc/performance-tuner/performance_usb',
                '/etc/performance-tuner/powersave_usb')

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        binder.bind_to_constructor('plugin.service.usb', functools.partial(
            Finder, path='/sys/bus/usb/devices'
        ))

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):

        storage.dispatch({
            'type': '@@app/dashboard/settings/performance/usb',
            'action': DashboardSettingsPerformance,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/dashboard/settings/powersave/usb',
            'action': DashboardSettingsPowersave,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/dashboard/properties/usb',
            'action': DashboardProperties,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/exporter/performance/usb',
            'action': self._performance
        })

        storage.dispatch({
            'type': '@@app/exporter/powersave/usb',
            'action': self._powersave
        })

        storage.dispatch({
            'type': '@@app/exporter/cleanup/usb',
            'action': self._cleanup
        })


module = Loader()
