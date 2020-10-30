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


def configure(binder: inject.Binder, options: {} = None, args: {} = None):
    from . import powersave
    from . import performance

    binder.bind('udev_rules.performance', performance.Container())
    binder.bind('udev_rules.powersave', powersave.Container())


def bootstrap(options: {} = None, args: [] = None):
    from modules import qt5_window

    @qt5_window.workspace(name='Udev rules', focus=False, position=1)
    def window_dashboard(parent=None, widget=None):
        from .workspace.dashboard import DashboardWidget
        return DashboardWidget()