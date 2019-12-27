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
import os
import stat
import inject

from string import Template

from PyQt5 import QtWidgets
from .gui.box import MessageBox


class ModuleActions(object):
    udev_rule = '/etc/udev/rules.d/70-performance.rules'

    @inject.params(window='window', container='container.exporter')
    def onActionSchemaApply(self, event=None, window=None, container=None):

        message = "<h2>Update udev rule?</h2> <p>{}</p><br/>".format(self.udev_rule)
        reply = MessageBox.question(window, 'Update udev rule?', message, MessageBox.Yes, MessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        errors = []

        try:
            with open(self.udev_rule, 'w') as stream:
                os.chmod(self.udev_rule, stat.S_IRUSR | stat.S_IWUSR |
                         stat.S_IXGRP | stat.S_IRGRP |
                         stat.S_IXOTH | stat.S_IROTH)
                template = Template(open('templates/udev.tpl', 'r').read())
                for exporter, priority in container.collection:
                    performance, powersave = exporter.cleanup()
                    if performance is None or powersave is None:
                        continue

                    name_performance, content = performance
                    if name_performance is None or content is None:
                        continue

                    name_powersave, content = powersave
                    if name_powersave is None or content is None:
                        continue

                    stream.write(template.substitute(
                        performance=name_performance,
                        powersave=name_powersave
                    ))

                stream.close()
        except (Exception) as ex:
            errors.append("{}".format(ex))

        if not len(errors): return None

        message = "<h2>Can not write udev rule:</h2> <p>{}</p><br/>".format("<br/>".join(errors))
        MessageBox.question(window, 'Can not write udev rule', message, MessageBox.Ok)

    @inject.params(window='window', container='container.exporter')
    def onActionSchemaCleanup(self, event=None, window=None, exporter=None):

        message = "<h2>Remove udev rule?</h2> <p>{}</p><br/>".format(self.udev_rule)
        reply = MessageBox.question(window, 'Remove udev rule?', message, MessageBox.Yes, MessageBox.No)
        if reply == QtWidgets.QMessageBox.No:
            return None

        errors = []

        try:
            if os.path.exists(self.udev_rule):
                os.remove(self.udev_rule)
        except (Exception) as ex:
            errors.append("{}".format(ex))

        message = "<h2>Can not remove udev rule:</h2> <p>{}</p><br/>".format("<br/>".join(errors))
        MessageBox.question(window, 'Can not remove udev rule', message, MessageBox.Ok)
