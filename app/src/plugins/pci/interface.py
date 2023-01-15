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

from modules import qt5_window
from modules import qt5_workspace_adapter
from modules import qt5_workspace_battery


@qt5_window.workspace(name='PCI', focus=False, position=2)
def window_workspace(parent=None):
    from .workspace.settings import SettingsWidget
    return SettingsWidget()


@qt5_workspace_battery.element()
def battery_element(parent=None):
    from .settings.panel import SettingsPowersaveWidget
    return SettingsPowersaveWidget()


@qt5_workspace_adapter.element()
def adapter_element(parent=None):
    from .settings.panel import SettingsPerformanceWidget
    return SettingsPerformanceWidget()

