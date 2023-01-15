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
    def __init__(self, path=None):
        self.path = path

    @property
    def name(self):
        path = "{}/name".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def code(self):
        return os.path.basename(self.path).replace(":","")

    @property
    def power_control(self):
        power_control = "{}/device/power/control".format(self.path)
        if not os.path.exists(power_control): return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

        return None


class Finder(object):
    def devices(self):
        context = pyudev.Context()
        for device in context.list_devices(subsystem='i2c'):
            yield Device('/sys{}'.format(device.get('DEVPATH')))
