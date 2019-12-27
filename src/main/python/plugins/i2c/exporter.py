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
import hexdi

from string import Template


class Exporter(object):
    name_performance = '/etc/performance-tuner/performance_i2c'
    name_powersave = '/etc/performance-tuner/powersave_i2c'

    def __init__(self, options=None, args=None):
        pass

    @hexdi.inject('config', 'plugin.service.i2c')
    def export(self, config=None, service=None):
        """

        :return:
        """
        ignored = []
        for device in service.cores():
            if int(config.get('i2c.managed.{}'.format(device.code), 1)):
                continue
            ignored.append(device.path)

        performance = Template(open('templates/i2c.tpl', 'r').read())
        powersave = Template(open('templates/i2c.tpl', 'r').read())

        return (
            (self.name_performance, performance.substitute(
                schema=config.get('i2c.performance', 'on'),
                ignored="'{}'".format("','".join(ignored))
            )),
            (self.name_powersave, powersave.substitute(
                schema=config.get('i2c.powersave', 'auto'),
                ignored="'{}'".format("','".join(ignored))
            ))
        )

    def cleanup(self):
        return (
            (self.name_performance, ''),
            (self.name_powersave, '')
        )
