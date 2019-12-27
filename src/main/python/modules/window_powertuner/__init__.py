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
import hexdi
import functools

from .gui.window import MainWindow
from .actions import ModuleActions
from .container import DashboardContainer
from .container import ExporterContainer


class Loader(object):
    actions = ModuleActions()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @hexdi.inject('config')
    def _constructor(self, config=None):
        widget = MainWindow()
        widget.resize_event.connect(self.actions.onActionWindowResize)
        widget.schema_cleanup.connect(self.actions.onActionSchemaCleanup)
        widget.schema_apply.connect(self.actions.onActionSchemaApply)

        width = int(config.get('window.width', 640))
        height = int(config.get('window.height', 480))
        widget.resize(width, height)

        return widget

    def enabled(self, options=None, args=None):
        return True

    def boot(self, options=None, args=None):
        container = hexdi.get_root_container()
        container.bind_type(self._constructor, 'window', hexdi.lifetime.PermanentLifeTimeManager)
        container.bind_type(DashboardContainer, 'container.dashboard', hexdi.lifetime.PermanentLifeTimeManager)
        container.bind_type(ExporterContainer, 'container.exporter', hexdi.lifetime.PermanentLifeTimeManager)


module = Loader()
