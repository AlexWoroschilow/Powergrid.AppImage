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
import glob


class Device(object):
    def __init__(self, path=None):
        self.path = path

    @property
    def power_level(self):
        path = "{}/power/level".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'r') as stream:
            return stream.read().strip("\n")

    @power_level.setter
    def power_level(self, value):
        path = "{}/power/level".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'w') as stream:
            stream.write('{}'.format(value))
            stream.close()

    @property
    def power_control(self):
        path = "{}/power/control".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'r') as stream:
            return stream.read().strip("\n")

    @power_control.setter
    def power_control(self, value):
        path = "{}/power/control".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'w') as stream:
            stream.write('{}'.format(value))
            stream.close()

    @property
    def power_autosuspend(self):
        value = "{}/power/autosuspend".format(self.path)
        if not os.path.exists(value):
            return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @power_autosuspend.setter
    def power_autosuspend(self, value):
        path = "{}/power/autosuspend".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'w') as stream:
            stream.write('{}'.format(value))
            stream.close()

    @property
    def power_autosuspend_timeout(self):
        value = "{}/power/autosuspend_delay_ms".format(self.path)
        if not os.path.exists(value):
            return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @power_autosuspend_timeout.setter
    def power_autosuspend_timeout(self, value):
        path = "{}/power/autosuspend_delay_ms".format(self.path)
        if not os.path.exists(path):
            return None

        with open(path, 'w') as stream:
            stream.write('{}'.format(value))
            stream.close()

    @property
    def vendor(self):
        value = "{}/idVendor".format(self.path)
        if not os.path.exists(value):
            return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def product(self):
        value = "{}/idProduct".format(self.path)
        if not os.path.exists(value):
            return None

        with open(value, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def code(self):
        return "{}{}".format(self.vendor, self.product)


class Finder(object):

    def __init__(self, path=None):
        self.path = path

    def __call__(self, *args, **kwargs):
        return self

    def devices(self):

        for device_path in glob.glob('{}/*'.format(self.path)):

            instance = Device(device_path)
            if instance.vendor is None:
                continue
            if instance.product is None:
                continue
            yield instance


if __name__ == "__main__":

    ignored = [$ignored]
    source = '/sys/bus/usb/devices'
    assert (os.path.exists(source))

    finder = Finder(source)
    for device in finder.devices():
        if device.code in ignored:
            continue

        device.power_control = '$power_control'
        device.power_level = '$power_level'

        device.power_autosuspend_timeout = '$autosuspend_delay'
        device.power_autosuspend = '$autosuspend'
