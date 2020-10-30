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

import inject


class Container(object):
    def __init__(self):
        self.collection = []

    def append(self, callback=None):
        assert (callable(callback))
        self.collection.append(callback)

    @property
    def rules(self):
        for callback in self.collection:
            for script in callback():
                yield 'SUBSYSTEM=="power_supply", ACTION=="change", ATTR{{online}}=="0", RUN+="{rule}"'. \
                    format(online='online', rule=script)


@inject.params(container='udev_rules.powersave')
def rule(*args, **kwargs):
    container = kwargs.get('container')

    def wrapper1(*args, **kwargs):
        container.append(args[0])

        return args[0]

    return wrapper1
