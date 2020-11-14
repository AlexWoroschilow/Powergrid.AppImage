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


def element(*args, **kwargs):
    @hexdi.inject('workspace.adapter')
    def wrapper1(*args, **kwargs):
        assert (callable(args[0]))

        widget_class = args[0]
        if not widget_class: return None

        from .settings import SettingsWidget
        workspace: SettingsWidget = args[1]
        if not workspace: return widget_class

        widget = widget_class(parent=workspace)
        workspace.addWidget(widget)

        return widget_class

    return wrapper1
