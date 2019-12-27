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

from .actions import ModuleActions
from .service import ServiceTheme


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(config='config')
    def _constructor_themes(self, config=None):
        themes_default = config.get('themes.default', 'themes/')
        themes_custom = config.get('themes.custom', '~/.config/AOD-Dictionary/themes')
        return ServiceTheme([themes_default, themes_custom])

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):
        binder.bind_to_constructor('themes', self._constructor_themes)


module = Loader()
