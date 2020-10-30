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
import functools

import inject
from PyQt5 import QtWidgets

from .actions import ModuleActions
from .workspace import toolbar
from .workspace import workspace
from .workspace.window import MainWindow


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    @inject.params(config='config', content='window.content', header='window.header')
    def _window(config, content: QtWidgets.QWidget, header: QtWidgets.QWidget, actions: ModuleActions):
        widget = MainWindow()

        widget.setCentralWidget(QtWidgets.QWidget())
        widget.centralWidget().setContentsMargins(0, 0, 0, 0)
        widget.centralWidget().setLayout(QtWidgets.QVBoxLayout())
        widget.centralWidget().layout().addWidget(header)
        widget.centralWidget().layout().addWidget(content)

        widget.resizeAction.connect(actions.resizeActionEvent)

        width = int(config.get('window.width', 400))
        height = int(config.get('window.height', 500))
        widget.resize(width, height)

        return widget

    binder.bind_to_constructor('window', functools.partial(
        _window, actions=ModuleActions()
    ))

    from .workspace.content import WindowContent
    binder.bind_to_constructor('window.content', WindowContent)

    from .workspace.header import ToolbarWidget
    binder.bind_to_constructor('window.header', ToolbarWidget)
