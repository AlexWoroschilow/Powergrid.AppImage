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

from .actions import ModuleActions


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def enabled(self):
        return True

    @inject.params(window='window')
    def boot(self, options=None, args=None, window=None):
        window.schema_cleanup.connect(self.actions.onActionSchemaCleanup)
        window.schema_apply.connect(self.actions.onActionSchemaApply)


module = Loader()
