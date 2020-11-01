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

import pyudev


class Device(object):
    def __init__(self, device=None):
        self.device = device

    @property
    def name(self):
        name = self.device.get('ID_MODEL_FROM_DATABASE')
        if not name: return self.path
        return (name.encode()).decode('unicode_escape')

    @property
    def path(self):
        return "/sys{}".format(self.device.get('DEVPATH'))

    @property
    def power_control(self):
        path = "{}/power/control".format(self.path)
        if not os.path.exists(path): return None

        with open(path, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def product(self):
        return self.device.get('PCI_ID')

    @property
    def vendor(self):
        return self.device.get('PCI_ID')

    @property
    def code(self):
        unique = self.device.get('PCI_ID')
        if not unique: return os.path.basename(self.path)
        return unique.replace(':', '.')


class Finder(object):
    def monitor(self):
        monitor = pyudev.Monitor.from_netlink(pyudev.Context())
        monitor.filter_by(subsystem='pci')
        monitor.start()
        for device in iter(monitor.poll, None):
            if not device.get('PCI_ID'): continue
            yield Device(device)

    def devices(self):
        context = pyudev.Context()
        for device in context.list_devices(subsystem='pci'):
            if not device.get('PCI_ID'): continue
            yield Device(device)
