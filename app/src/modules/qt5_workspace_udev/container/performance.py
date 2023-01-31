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


class Container(object):
    def __init__(self):
        self.collection = []

    def append(self, callback=None):
        assert (callable(callback))
        self.collection.append(callback)


@hexdi.permanent('rules.performance')
class ContainerPerformanceRules(Container):

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
