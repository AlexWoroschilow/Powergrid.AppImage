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
    name_performance = '/etc/performance-tuner/performance_usb'
    name_powersave = '/etc/performance-tuner/powersave_usb'

    def __init__(self, options=None, args=None):
        pass

    @inject.params(config='config', service='plugin.service.usb')
    def export(self, config=None, service=None):
        """

        :return:
        """
        powersave_ignored = []
        performance_ignored = []
        for device in service.devices():
            value_ignored = config.get('usb.permanent.{}'.format(device.code), 0)
            if not int(value_ignored):
                continue
            if int(value_ignored) == 1:
                performance_ignored.append(device.code)
                continue
            if int(value_ignored) == 2:
                powersave_ignored.append(device.code)
                continue

        performance = Template(open('templates/usb.tpl', 'r').read())
        powersave = Template(open('templates/usb.tpl', 'r').read())

        return (
            (self.name_performance, performance.substitute(
                power_level=config.get('usb.performance.power_level', 'on'),
                power_control=config.get('usb.performance.power_control', 'on'),
                autosuspend_delay=config.get('usb.performance.autosuspend_delay', '-1'),
                autosuspend=config.get('usb.performance.autosuspend', '-1'),
                ignored="'{}'".format("','".join(performance_ignored))
            )),
            (self.name_powersave, powersave.substitute(
                power_level=config.get('usb.powersave.power_level', 'auto'),
                power_control=config.get('usb.powersave.power_control', 'auto'),
                autosuspend_delay=config.get('usb.powersave.autosuspend_delay', '500'),
                autosuspend=config.get('usb.powersave.autosuspend', '500'),
                ignored="'{}'".format("','".join(powersave_ignored))
            ))
        )

    def cleanup(self):
        return (
            (self.name_performance, ''),
            (self.name_powersave, '')
        )
