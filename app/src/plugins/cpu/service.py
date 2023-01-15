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

import hexdi

from .device.cpu import Device


@hexdi.permanent('plugin.service.cpu')
class Finder(object):
    def devices(self):
        import pyudev
        context = pyudev.Context()
        for device in context.list_devices(subsystem='cpu'):
            yield Device('/sys{}'.format(device.get('DEVPATH')))
