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


class Device(object):
    def __init__(self, device=None):
        self.device = device

    @property
    def name(self):
        return self.device.get('ID_MODEL_FROM_DATABASE')

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
        return self.device.get('PCI_ID'). \
            replace(':', '.')


class Finder(object):
    def devices(self):
        import pyudev
        context = pyudev.Context()
        for device in context.list_devices(subsystem='pci'):
            yield Device(device)
