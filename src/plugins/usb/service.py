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

import pyudev


class Device(pyudev.Device):
    def __init__(self, device):
        self.device = device

    @property
    def name(self):
        name = self.device.get('ID_MODEL_ENC')
        if not name: return self.path
        return (name.encode()).decode('unicode_escape')

    @property
    def action(self):
        return self.device.action

    @property
    def path(self):
        return "/sys{}".format(self.device.get('DEVPATH'))

    @property
    def power_level(self):
        value = "{}/power/level".format(self.path)
        if not os.path.exists(value): return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def power_control(self):
        value = "{}/power/control".format(self.path)
        if not os.path.exists(value):
            return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def power_autosuspend(self):
        value = "{}/power/autosuspend".format(self.path)
        if not os.path.exists(value): return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def power_autosuspend_timeout(self):
        value = "{}/power/autosuspend_delay_ms".format(self.path)
        if not os.path.exists(value): return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def vendor(self):
        return self.device.get('ID_VENDOR')

    @property
    def product(self):
        return self.device.get('ID_MODEL')

    @property
    def code(self):
        return "{}{}{}".format(
            self.device.get('ID_VENDOR_ID'),
            self.device.get('ID_MODEL_ID'),
            self.device.get('ID_REVISION')
        )


class Finder(object):

    def monitor(self):
        monitor = pyudev.Monitor.from_netlink(pyudev.Context())
        monitor.filter_by(subsystem='usb')
        monitor.start()
        for device in iter(monitor.poll, None):
            if not device.get('ID_VENDOR_ID'): continue
            if not device.get('ID_MODEL_ID'): continue
            yield Device(device)

    def devices(self):
        context = pyudev.Context()
        for device in context.list_devices(subsystem='usb'):
            if not device.get('ID_VENDOR_ID'): continue
            if not device.get('ID_MODEL_ID'): continue
            yield Device(device)
