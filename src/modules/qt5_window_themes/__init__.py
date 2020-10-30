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
from .service import ServiceTheme


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    @inject.params(config='config')
    def _constructor(config=None):
        return ServiceTheme([config.get('themes.default', 'themes/')])

    binder.bind_to_constructor('themes', _constructor)


def bootstrap(options: {} = None, args: [] = None, window=None):
    from modules import qt5_window

    @qt5_window.toolbar(name='Themes', focus=False, position=6)
    def window_toolbar(parent=None):
        from .toolbar.panel import ToolbarWidget

        widget = ToolbarWidget()
        parent.actionReload.connect(widget.reload)
        return widget
