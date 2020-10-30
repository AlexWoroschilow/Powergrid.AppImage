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
import functools
import os

import inject

from .services import DeviceLocator


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    binder.bind_to_constructor('usbids', functools.partial(
        DeviceLocator, file="{}/usb.ids.txt".format(os.path.dirname(os.path.realpath(__file__)))
    ))

    binder.bind_to_constructor('pciids', functools.partial(
        DeviceLocator, file="{}/pci.ids.txt".format(os.path.dirname(os.path.realpath(__file__)))
    ))
