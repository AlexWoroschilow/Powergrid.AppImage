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
import glob
import hexdi


class Device(object):
    def __init__(self, path=None):
        self.path = path

    @property
    @hexdi.inject('usbids')
    def name(self, usbids=None):
        product = "{}/product".format(self.path)
        if not os.path.exists(product):
            return usbids.get(self.vendor, self.product)

        with open(product, 'r') as stream:
            return stream.read().strip(" \n")
        return usbids.get(self.vendor, self.product)

    @property
    def power_level(self):
        power_control = "{}/power/level".format(self.path)
        if not os.path.exists(power_control):
            return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def power_control(self):
        power_control = "{}/power/control".format(self.path)
        if not os.path.exists(power_control):
            return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def power_autosuspend(self):
        power_control = "{}/power/autosuspend".format(self.path)
        if not os.path.exists(power_control):
            return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def power_autosuspend_timeout(self):
        power_control = "{}/power/autosuspend_delay_ms".format(self.path)
        if not os.path.exists(power_control):
            return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def vendor(self):
        power_control = "{}/idVendor".format(self.path)
        if not os.path.exists(power_control):
            return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def product(self):
        power_control = "{}/idProduct".format(self.path)
        if not os.path.exists(power_control):
            return None

        with open(power_control, 'r') as stream:
            return stream.read().strip("\n")

    @property
    def code(self):
        return "{}{}".format(self.vendor, self.product)


class Finder(object):

    def __init__(self, path=None):
        self.path = path
        pass

    def __call__(self, *args, **kwargs):
        return self

    def cores(self):

        for device in glob.glob('{}/*'.format(self.path)):

            instance = Device(device)
            if instance.vendor is None:
                continue
            if instance.product is None:
                continue
            yield instance
