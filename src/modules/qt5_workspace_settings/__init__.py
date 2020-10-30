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
from PyQt5 import QtWidgets

from .workspace import element


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    @inject.params(window='window')
    def _constructor(window: QtWidgets.QWidget):
        from .workspace.settings import SettingsWidget
        widget = SettingsWidget()
        return widget

    binder.bind_to_constructor('workspace.settings', _constructor)


def bootstrap(options: {} = None, args: [] = None, window=None):
    from modules import qt5_window

    @qt5_window.workspace(name='Schema', focus=False, position=1)
    @inject.params(widget='workspace.settings')
    def window_dashboard(parent=None, widget=None):
        return widget

    @qt5_window.toolbar(name='Schema', focus=True, position=0)
    def window_toolbar(parent=None):
        from .toolbar.panel import ToolbarWidget
        from . import actions

        widget = ToolbarWidget()
        widget.actionPerformance.connect(actions.onActionPerformace)
        widget.actionPowersave.connect(actions.onActionPowersave)
        return widget
