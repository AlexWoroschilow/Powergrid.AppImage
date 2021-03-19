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


class Device(object):
    def __init__(self, path=None):
        self.path = path
        self._name = None

    @property
    def name(self):
        if self._name is not None:
            return self._name
        name = os.path.basename(self.path)
        self._name = name.capitalize()
        return self._name

    @property
    def code(self):
        return self.name.lower()

    @property
    def governors(self):
        with open("{}/cpufreq/scaling_available_governors".format(self.path), 'r') as stream:
            governors = stream.read()
            governors = governors.strip("\n")
            return governors.split(' ')

    @property
    def governor(self):
        with open("{}/cpufreq/scaling_governor".format(self.path), 'r') as stream:
            return stream.read().strip("\n")

    @property
    def load(self):
        return self.frequence / self.frequence_max * 100

    @property
    def frequence(self):
        with open("{}/cpufreq/scaling_cur_freq".format(self.path), 'r') as stream:
            return int(stream.read().strip("\n"))

    @property
    def frequence_max(self):
        with open("{}/cpufreq/scaling_max_freq".format(self.path), 'r') as stream:
            return int(stream.read().strip("\n"))

    @property
    def frequence_min(self):
        with open("{}/cpufreq/scaling_min_freq".format(self.path), 'r') as stream:
            return int(stream.read().strip("\n"))

    def __gt__(self, other):
        a = re.sub('[^0-9]', '', self.name)
        b = re.sub('[^0-9]', '', other.name)
        return int(a) > int(b)

    def __lt__(self, other):
        a = re.sub('[^0-9]', '', self.name)
        b = re.sub('[^0-9]', '', other.name)
        return int(a) < int(b)

    def __eq__(self, other):
        a = re.sub('[^0-9]', '', self.name)
        b = re.sub('[^0-9]', '', other.name)
        return int(a) == int(b)


class Finder(object):
    def devices(self):
        import pyudev
        context = pyudev.Context()
        for device in context.list_devices(subsystem='cpu'):
            yield Device('/sys{}'.format(device.get('DEVPATH')))
