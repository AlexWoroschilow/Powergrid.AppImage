# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
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

from . import performance
from . import powersave
from .container import Container
from .dumper import DumperCleaner
from .dumper import DumperExport
from .dumper import DumperPerformance
from .dumper import DumperPowersave
from .dumper import DumperSchema


@hexdi.permanent('udev_dumper.schema')
class DumperSchemaInstance(DumperSchema):
    pass


@hexdi.permanent('udev_dumper.cleaner')
class DumperCleanerInstance(DumperCleaner):
    pass


@hexdi.permanent('udev_dumper.export')
class DumperExportInstance(DumperExport):
    pass


@hexdi.permanent('udev_dumper.performance')
class DumperPerformanceInstance(DumperPerformance):
    pass


@hexdi.permanent('udev_dumper.powersave')
class DumperPowersaveInstance(DumperPowersave):
    pass


@hexdi.permanent('rules.performance')
class ContainerPerformanceRules(Container):
    @property
    def rules(self):
        for callback in self.collection:
            for script in callback():
                yield script


@hexdi.permanent('rules.powersave')
class ContainerPowersaveRules(Container):
    @property
    def rules(self):
        for callback in self.collection:
            for script in callback():
                yield script


@hexdi.permanent('udev_rules.performance')
class ContainerPerformanceRulesUdev(object):
    @property
    @hexdi.inject('rules.performance')
    def rules(self, collection):
        for script in collection.rules:
            yield 'SUBSYSTEM=="power_supply", ACTION=="change", ATTR{{online}}=="1", RUN+="{}"'. \
                format("/bin/sh -c \\\"{}\\\" ".format(script))


@hexdi.permanent('udev_rules.powersave')
class ContainerPowerSaveRulesUdev(Container):
    @property
    @hexdi.inject('rules.powersave')
    def rules(self, collection):
        for script in collection.rules:
            yield 'SUBSYSTEM=="power_supply", ACTION=="change", ATTR{{online}}=="0", RUN+="{}"'. \
                format("/bin/sh -c \\\"{}\\\" ".format(script))
