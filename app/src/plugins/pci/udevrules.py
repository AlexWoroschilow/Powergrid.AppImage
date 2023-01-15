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

from modules.qt5_workspace_udev import performance
from modules.qt5_workspace_udev import powersave


@performance.rule()
@hexdi.inject('config', 'plugin.service.pci')
def rule_performance(config, service):
    for device in service.devices():
        permanent = config.get('pci.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/power/control'.format(device.path)
        if not os.path.exists(file): continue

        schema = config.get('default.performance.pci')
        schema = config.get('pci.performance', schema)
        schema = config.get('default.powersave.pci') if int(permanent) == 1 else schema
        schema = config.get('default.performance.pci') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)


@powersave.rule()
@hexdi.inject('config', 'plugin.service.pci')
def rule_powersave(config, service):
    for device in service.devices():
        permanent = config.get('pci.permanent.{}'.format(device.code), 0)
        if not os.path.exists(device.path): continue

        file = '{}/power/control'.format(device.path)
        if not os.path.exists(file): continue

        schema = config.get('default.powersave.pci')
        schema = config.get('pci.powersave', schema)
        schema = config.get('default.powersave.pci') if int(permanent) == 1 else schema
        schema = config.get('default.performance.pci') if int(permanent) == 2 else schema
        yield 'ls {} && echo {} > {}'.format(device.path, schema, file)
