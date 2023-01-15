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
import pyudev

from .device.disc import Device


@hexdi.permanent('plugin.service.disc')
class Finder(object):
    def monitor(self):
        monitor = pyudev.Monitor.from_netlink(pyudev.Context())
        monitor.filter_by(subsystem='block')
        monitor.start()
        for device in iter(monitor.poll, None):
            yield Device(device)

    def devices(self):
        context = pyudev.Context()
        for device in context.list_devices(DEVTYPE='disk'):
            if not device.get('ID_SERIAL'): continue
            yield Device(device)
