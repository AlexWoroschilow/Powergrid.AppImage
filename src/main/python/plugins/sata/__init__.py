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

from .service import Finder
from .exporter import Exporter


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def enabled(self):
        return True

    def configure(self, binder, options, args):
        """
        Setup plugin services
        :param binder:
        :param options:
        :param args:
        :return:
        """
        from .service import Finder

        binder.bind_to_constructor('plugin.service.sata', functools.partial(
            Finder, path='/sys/class/scsi_host'
        ))

    @inject.params(performance='container.dashboard.performance', powersave='container.dashboard.powersave',
                   devices='container.dashboard.devices', container_exporter='container.exporter')
    def boot(self, options=None, args=None, performance=None, powersave=None, devices=None,
             container_exporter=None):
        """
        Define the services and setup the service-container
        :param options:
        :param args:
        :param performance:
        :param container_exporter:
        :return:
        """
        from .gui.settings.settings import DashboardSettingsPerformance
        performance.append(DashboardSettingsPerformance, 0)

        from .gui.settings.settings import DashboardSettingsPowersave
        powersave.append(DashboardSettingsPowersave, 0)

        from .gui.devices.properties import DashboardProperties
        devices.append(DashboardProperties, 0)

        from .exporter import Exporter
        container_exporter.append(Exporter(options, args), 0)

module = Loader()
