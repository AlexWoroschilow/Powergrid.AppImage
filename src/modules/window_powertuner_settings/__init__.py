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
import functools
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from .gui.widget import SettingsWidget
from .actions import SettingsActions
from .gui.menu import SettingsMenu


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(window='window')
    def _on_action_settings(self, event, window):
        menu = QtWidgets.QMenu()
        menu.addAction(SettingsMenu(window))
        menu.exec_(QtGui.QCursor.pos())

    def enabled(self, options=None, args=None):
        return True

    def configure(self, binder, options, args):
        from .factory import SettingsFactory
        binder.bind_to_constructor('settings.factory', SettingsFactory)

    @inject.params(window='window')
    def boot(self, options, args, window=None):
        window.settingsAction.connect(self._on_action_settings)


module = Loader()
