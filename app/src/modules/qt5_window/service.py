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
from PyQt5 import QtWidgets

from .actions import ModuleActions
from .dialog.message import MessageBox
from .workspace import toolbar
from .workspace import workspace
from .workspace.content import WindowContent
from .workspace.header import HeaderWidget
from .workspace.window import MainWindow


@hexdi.permanent('window.content')
class WindowContentInstance(WindowContent):
    pass


@hexdi.permanent('window.header')
class WindowContentInstance(HeaderWidget):
    pass


@hexdi.permanent('window.actions')
class ModuleActionsInstance(ModuleActions):
    pass


@hexdi.permanent('window')
class MainWindowInstance(MainWindow):
    @hexdi.inject('config', 'window.header', 'window.content', 'window.actions')
    def __init__(self, config, header, content, actions):
        super(MainWindowInstance, self).__init__()

        class CentralWidget(QtWidgets.QFrame):
            def __init__(self):
                super(CentralWidget, self).__init__()
                self.setLayout(QtWidgets.QVBoxLayout())
                self.layout().setContentsMargins(0, 0, 0, 0)
                self.layout().setSpacing(0)

        self.setCentralWidget(CentralWidget())
        self.centralWidget().setContentsMargins(0, 0, 0, 0)
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())
        self.centralWidget().layout().addWidget(header)
        self.centralWidget().layout().addWidget(content)

        self.resizeAction.connect(actions.resizeActionEvent)

        width = int(config.get('window.width', 400))
        height = int(config.get('window.height', 500))
        self.resize(width, height)


@hexdi.permanent('window.dialog_manager')
class ModuleActionsInstance(object):

    @hexdi.inject('window')
    def execute(self, file=None, window=None):
        if not file: return None

        message_content = open(file, 'r').read()
        message_content = message_content.replace("\n", "<br/>")
        message = "<h2>Execute optimisation script?</h2> <p>{}</p><br/>".format(message_content)
        result = MessageBox(window, 'Execute optimisation script?', message, MessageBox.Ok, MessageBox.Cancel)
        return result.exec_()

    @hexdi.inject('window')
    def error(self, message=None, window=None):
        message = "<h2>Can not execute optimisation script:</h2> <p>{}</p><br/>".format(message)
        return MessageBox.question(window, 'Can not execute optimisation script', message, MessageBox.Ok)
