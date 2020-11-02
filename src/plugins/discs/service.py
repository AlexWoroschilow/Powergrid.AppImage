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
import re

import pyudev


class Device(object):
    def __init__(self, device=None):
        self.device = device

    @property
    def path(self):
        return '/sys{}'.format(self.device.get('DEVPATH'))

    @property
    def name(self):
        name = self.device.get('ID_MODEL_ENC')
        if not name: return self.path
        return (name.encode()).decode('unicode_escape')

    @property
    def action(self):
        return self.device.action

    @property
    def power_control(self):
        power_control = "{}/power/control".format(self.path)
        if not os.path.exists(power_control): return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

        return None

    @property
    def code(self):
        serial = self.device.get('ID_SERIAL')
        return re.sub(r"(?x)\.?-?_?;?:?/?\|?\\?", "", serial)


class Finder(object):
    def monitor(self):
        monitor = pyudev.Monitor.from_netlink(pyudev.Context())
        monitor.filter_by(subsystem='block')
        monitor.start()
        for device in iter(monitor.poll, None):
            yield Device(device)

    def devices(self):
        context = pyudev.Context()
        for device in context.list_devices(DEVTYPE='disk'):
            if not device.get('ID_SERIAL'): continue
            print(device)
            yield Device(device)
