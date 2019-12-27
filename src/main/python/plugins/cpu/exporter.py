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
    path_performance = '/etc/performance-tuner/performance_cpu'
    path_powersave = '/etc/performance-tuner/powersave_cpu'

    def __init__(self, options=None, args=None):
        pass

    @inject.params(config='config', service='plugin.service.cpu')
    def export(self, config=None, service=None):
        """

        :return:
        """
        service

        ignored = []
        for device in service.cores():
            if int(config.get('cpu.managed.{}'.format(device.code), 1)):
                continue
            ignored.append(device.path)

        performance = Template(open('templates/cpu.tpl', 'r').read())
        powersave = Template(open('templates/cpu.tpl', 'r').read())

        return (
            (self.path_performance, performance.substitute(
                schema=config.get('cpu.performance', 'ondemand'),
                ignored="'{}'".format("','".join(ignored))
            )),
            (self.path_powersave, powersave.substitute(
                schema=config.get('cpu.powersave', 'powersave'),
                ignored="'{}'".format("','".join(ignored))
            ))
        )

    def cleanup(self):
        return (
            (self.path_performance, ''),
            (self.path_powersave, '')
        )
