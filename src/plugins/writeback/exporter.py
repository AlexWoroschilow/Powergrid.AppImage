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
    name_performance = '/etc/performance-tuner/performance_writeback'
    name_powersave = '/etc/performance-tuner/powersave_writeback'

    def __init__(self, options=None, args=None):
        pass

    @inject.params(config='config')
    def export(self, config=None):
        """

        :return:
        """
        performance = Template(open('templates/writeback.tpl', 'r').read())
        powersave = Template(open('templates/writeback.tpl', 'r').read())

        return (
            (self.name_performance, performance.substitute(
                schema=config.get('writeback.performance', '')
            )),
            (self.name_powersave, powersave.substitute(
                schema=config.get('writeback.powersave', '1500')
            ))
        )

    def cleanup(self):
        return (
            (self.name_performance, ''),
            (self.name_powersave, '')
        )
