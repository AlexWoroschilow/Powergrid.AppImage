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


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config', service='plugin.service.hda')
    def _ignores(self, status=1, config=None, service=None):
        ignored = []
        for device in service.devices():
            value_ignored = config.get('hda.permanent.{}'.format(device.name), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == status:
                ignored.append(device.code)
                continue
        return ignored

    @inject.params(config='config')
    def _performance(self, config=None):
        with open('templates/hda.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/performance_hda', template.substitute(
                schema=config.get('hda.performance', ''),
                ignored="'{}'".format("','".join(self._ignores(1)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _powersave(self, config=None):
        with open('templates/hda.tpl', 'r') as stream:
            template = Template(stream.read())
            return ('/etc/performance-tuner/powersave_hda', template.substitute(
                schema=config.get('hda.powersave', '1'),
                ignored="'{}'".format("','".join(self._ignores(2)))
            ))

        return (None, None)

    @inject.params(config='config')
    def _cleanup(self, config=None):
        return ('/etc/performance-tuner/performance_hda',
                '/etc/performance-tuner/powersave_hda')

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        binder.bind_to_constructor('plugin.service.hda', functools.partial(
            Finder, path='/sys/module/snd_hda_intel'
        ))

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):

        storage.dispatch({
            'type': '@@app/dashboard/settings/performance/hda',
            'action': DashboardSettingsPerformance,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/dashboard/settings/powersave/hda',
            'action': DashboardSettingsPowersave,
            'priority': 0,
        })

        storage.dispatch({
            'type': '@@app/exporter/performance/hda',
            'action': self._performance
        })

        storage.dispatch({
            'type': '@@app/exporter/powersave/hda',
            'action': self._powersave
        })

        storage.dispatch({
            'type': '@@app/exporter/cleanup/hda',
            'action': self._cleanup
        })


module = Loader()
