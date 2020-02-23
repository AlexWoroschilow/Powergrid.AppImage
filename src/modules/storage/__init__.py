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
import inject
import functools
import pydux


class Storage(object):
    _performance = []
    _powersave = []
    _cleanup = []

    @property
    def performance(self):
        return self._performance

    @property
    def powersave(self):
        return self._powersave

    @property
    def cleanup(self):
        return self._cleanup

    @performance.setter
    def performance(self, bunch):
        self.performance.append(bunch)

    @powersave.setter
    def powersave(self, bunch):
        self.powersave.append(bunch)

    @cleanup.setter
    def cleanup(self, bunch):
        self.cleanup.append(bunch)


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        binder.bind('storage', pydux.create_store(self.storage))

    def storage(self, state=None, action=None):

        state = Storage() \
            if state is None \
            else state

        if 'type' not in action.keys():
            raise Exception('type is required')

        if 'action' not in action.keys():
            return state

        if action['type'].find('/exporter/performance') != -1:
            state.performance.append(action['action'])

        if action['type'].find('/exporter/powersave') != -1:
            state.powersave.append(action['action'])

        if action['type'].find('/exporter/cleanup') != -1:
            state.cleanup.append(action['action'])

        return state


module = Loader()
