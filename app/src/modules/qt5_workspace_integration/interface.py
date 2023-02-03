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


@qt5_window.toolbar(name='System integration', focus=True, position=0)
def window_toolbar(parent=None):
    """
    Display a toolbar at the top of the window
    """
    from .toolbar.panel import ToolbarWidget
    from . import actions

    widget = ToolbarWidget()
    widget.actionApply.connect(actions.onActonApply)

    return widget
