#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITION
import os
import sys
import glob


class Device(object):
    def __init__(self, path=None):
        self.path = path

    @property
    def name(self):
        name = os.path.basename(self.path)
        return name.capitalize()

    @property
    def power_control(self):
        path = "{}/link_power_management_policy".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'r') as stream:
            return stream.read().strip("\n")

    @power_control.setter
    def power_control(self, value):
        path = "{}/link_power_management_policy".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'w') as stream:
            stream.write('{}'.format(value))
            stream.close()

    @property
    def code(self):
        return self.name.lower()


class Finder(object):

    def __init__(self, path=None):
        self.path = path
        pass

    def __call__(self, *args, **kwargs):
        return self

    def devices(self):
        for device in glob.glob('{}/*'.format(self.path)):
            yield Device(device)


if __name__ == "__main__":

    ignored = [$ignored]
    source = '/sys/class/scsi_host'
    assert (os.path.exists(source))

    finder = Finder(source)
    for device in finder.devices():
        if device.code in ignored:
            continue

        device.power_control = '$schema'
