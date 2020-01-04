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

from string import Template


class Exporter(object):
    name_performance = '/etc/performance-tuner/performance_pci'
    name_powersave = '/etc/performance-tuner/powersave_pci'

    def __init__(self, options=None, args=None):
        pass

    @inject.params(config='config', service='plugin.service.pci')
    def export(self, config=None, service=None):
        """

        :return:
        """
        powersave_ignored = []
        performance_ignored = []
        for device in service.cores():
            value_ignored = config.get('pci.permanent.{}'.format(device.code), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == 1:
                performance_ignored.append(device.code)
                continue
            if int(value_ignored) == 2:
                powersave_ignored.append(device.code)
                continue

        performance = Template(open('templates/pci.tpl', 'r').read())
        powersave = Template(open('templates/pci.tpl', 'r').read())

        return (
            (self.name_performance, performance.substitute(
                schema=config.get('pci.performance', 'on'),
                ignored="'{}'".format("','".join(performance_ignored))
            )),
            (self.name_powersave, powersave.substitute(
                schema=config.get('pci.powersave', 'auto'),
                ignored="'{}'".format("','".join(powersave_ignored))
            ))
        )

    def cleanup(self):
        return (
            (self.name_performance, ''),
            (self.name_powersave, '')
        )
