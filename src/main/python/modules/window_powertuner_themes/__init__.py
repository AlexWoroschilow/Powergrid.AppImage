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

    def _constructor_settings(self):
        from .gui.settings.themes import WidgetSettingsThemes
        widget = WidgetSettingsThemes()
        widget.theme.connect(functools.partial(
            self.actions.on_action_theme, widget=widget
        ))
        return widget

    @inject.params(config='config')
    def _constructor_themes(self, config=None):
        return ServiceTheme([config.get('themes.default', 'themes/')])

    def enabled(self, options=None, args=None):
        return options.console is None

    def configure(self, binder, options, args):
        binder.bind_to_constructor('themes', self._constructor_themes)

    # @inject.params(factory='settings.factory')
    # def boot(self, options, args, factory=None):
    #     factory.addWidget(self._constructor_settings, 128)


module = Loader()
