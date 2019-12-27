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
import hexdi
import functools

from .services import DeviceLocator


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def enabled(self):
        return True

    def boot(self, options=None, args=None):
        container = hexdi.get_root_container()
        container.bind_type(functools.partial(
            DeviceLocator, file="{}/usb.ids.txt".format(os.path.dirname(os.path.realpath(__file__)))
        ), 'usbids', hexdi.lifetime.PermanentLifeTimeManager)

        container.bind_type(functools.partial(
            DeviceLocator, file="{}/pci.ids.txt".format(os.path.dirname(os.path.realpath(__file__)))
        ), 'pciids', hexdi.lifetime.PermanentLifeTimeManager)


module = Loader()
