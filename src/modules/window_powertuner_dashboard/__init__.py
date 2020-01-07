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
from .container import DashboardContainerHorizontal
from .container import DashboardContainerVertical


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @inject.params(window='window')
    def __constructor(self, window=None):
        from .gui.dashboard.widget import DashboardWidget

        widget = DashboardWidget()
        widget.settingsAction.connect(window.settingsAction.emit)

        return widget

    def configure(self, binder, options, args):
        binder.bind_to_constructor('container.dashboard.performance', DashboardContainerHorizontal)
        binder.bind_to_constructor('container.dashboard.powersave', DashboardContainerHorizontal)
        binder.bind_to_constructor('container.dashboard.devices', DashboardContainerVertical)

    @inject.params(container_dashboard='container.dashboard')
    def boot(self, options=None, args=None, container_dashboard=None):
        """
        Define the services and setup the service-container
        :param options:
        :param args:
        :param container_dashboard:
        :return:
        """

        container_dashboard.append(self.__constructor, 0)


module = Loader()
