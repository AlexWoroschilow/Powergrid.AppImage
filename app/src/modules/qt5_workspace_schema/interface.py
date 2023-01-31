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

from modules import qt5_window
from .toolbar.panel import ToolbarWidget


@qt5_window.workspace(name='Schema', focus=True, position=0)
@hexdi.inject('workspace.settings')
def window_dashboard(parent=None, widget=None):
    return widget


@qt5_window.toolbar(name='Schema', focus=False, position=2)
def window_toolbar(parent=None):
    from . import actions

    widget = ToolbarWidget()
    widget.actionPerformance.connect(actions.onActionPerformace)
    widget.actionPerformanceExport.connect(actions.onActionPerformaceExport)
    widget.actionPowersave.connect(actions.onActionPowersave)
    widget.actionPowersaveExport.connect(actions.onActionPowersaveExport)
    return widget
