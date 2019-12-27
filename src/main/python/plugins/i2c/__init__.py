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

from .service import Finder
from .exporter import Exporter


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def _constructor_widget(self, options=None, args=None):
        from .gui.dashboard.widget import DashboardWidget

        widget = DashboardWidget()
        return widget

    @property
    def enabled(self):
        return True

    @hexdi.inject('container.dashboard', 'container.exporter')
    def boot(self, options=None, args=None, container_dashboard=None, container_exporter=None):
        """
        Define the services and setup the service-container
        :param options:
        :param args:
        :param container_dashboard:
        :param container_exporter:
        :return:
        """
        container = hexdi.get_root_container()
        container.bind_type(functools.partial(
            Finder, path='/sys/bus/i2c/devices'
        ), 'plugin.service.i2c', hexdi.lifetime.PermanentLifeTimeManager)

        container_dashboard.append(functools.partial(
            self._constructor_widget,
            options=options, args=args
        ), 10)

        container_exporter.append(Exporter(options, args), 0)



module = Loader()
