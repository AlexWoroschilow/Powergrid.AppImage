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
import pydux
import inject


class StorageExporter(object):
    powersave = []
    performance = []
    cleanup = []


class StorageSettings(object):
    performance = []
    powersave = []


class Storage(object):
    def __init__(self):
        self.settings = StorageSettings()
        self.exporter = StorageExporter()
        self.devices = []

    @property
    def performance(self):
        return self.exporter.performance

    @property
    def powersave(self):
        return self.exporter.powersave

    @property
    def cleanup(self):
        return self.exporter.cleanup


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def __test(self):
        return pydux.create_store(self.storage)

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        binder.bind_to_constructor('storage', self.__test)

    def storage(self, state=None, action=None):

        state = Storage() \
            if state is None \
            else state

        if 'type' not in action.keys():
            raise Exception('type is required')

        action_type = action['type']
        if 'action' not in action.keys():
            return state

        if action_type.find('/exporter/performance') != -1:
            state.exporter.performance.append(action['action'])

        if action_type.find('/exporter/powersave') != -1:
            state.exporter.powersave.append(action['action'])

        if action_type.find('/exporter/cleanup') != -1:
            state.exporter.cleanup.append(action['action'])

        if action_type.find('/dashboard/settings/performance') != -1:
            bunch = (action['action'], action['priority'])
            state.settings.performance.append(bunch)

        if action_type.find('/dashboard/settings/powersave') != -1:
            bunch = (action['action'], action['priority'])
            state.settings.powersave.append(bunch)

        if action_type.find('/dashboard/properties') != -1:
            bunch = (action['action'], action['priority'])
            state.devices.append(bunch)

        return state


module = Loader()
