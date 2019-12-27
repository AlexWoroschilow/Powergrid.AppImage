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

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .gui.box import MessageBox


class ModuleActions(object):

    @inject.params(config='config')
    def onActionWindowResize(self, event=None, config=None):
        config.set('window.width', '%s' % event.size().width())
        config.set('window.height', '%s' % event.size().height())
        return event.accept()

    @inject.params(window='window', container='container.exporter')
    def onActionSchemaApply(self, event=None, window=None, container=None):

        files = []
        for exporter, priority in container.collection:
            performance, powersave = exporter.cleanup()
            file, content = performance
            files.append(file)
            file, content = powersave
            files.append(file)

        message = "<h2>Write optimisation scripts?</h2> <p>{}</p><br/>".format("<br/>".join(files))
        reply = MessageBox.question(window, 'Write optimisation scripts?', message, MessageBox.Ok, MessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Cancel:
            return None

        errors = []
        for exporter, priority in container.collection:
            performance, powersave = exporter.export()
            if performance is None and powersave is None:
                continue

            try:
                file, content = performance
                folder = os.path.dirname(file)
                if not os.path.exists(folder):
                    os.mkdir(folder, 755)

                with open(file, 'w') as stream:
                    os.chmod(file, stat.S_IRUSR | stat.S_IWUSR |
                             stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                             stat.S_IXOTH | stat.S_IROTH)
                    stream.write(content)
                    stream.close()

            except (Exception) as ex:
                print(ex)

            try:
                file, content = powersave
                folder = os.path.dirname(file)
                if not os.path.exists(folder):
                    os.mkdir(folder, 755)

                with open(file, 'w') as stream:
                    os.chmod(file, stat.S_IRUSR | stat.S_IWUSR |
                             stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                             stat.S_IXOTH | stat.S_IROTH)
                    stream.write(content)
                    stream.close()

            except (Exception) as ex:
                errors.append("{}".format(ex))

        if not len(errors): return None

        message = "<h2>Can not write files:</h2> <p>{}</p><br/>".format("<br/>".join(errors))
        MessageBox.question(window, 'Can not write files', message, MessageBox.Ok)

    @inject.params(window='window', container='container.exporter')
    def onActionSchemaCleanup(self, event=None, window=None, container=None):

        files = []
        for exporter, priority in container.collection:
            performance, powersave = exporter.cleanup()
            file, content = performance
            files.append(file)
            file, content = powersave
            files.append(file)

        message = "<h2>Remove optimisation scripts?</h2> <p>{}</p><br/>".format("<br/>".join(files))
        reply = MessageBox.question(window, 'Remove optimisation scripts?', message, MessageBox.Ok, MessageBox.Cancel)
        if reply == QtWidgets.QMessageBox.Cancel:
            return None

        errors = []
        for exporter, priority in container.collection:
            performance, powersave = exporter.cleanup()

            try:

                file, content = performance
                if os.path.exists(file):
                    os.remove(file)

                file, content = powersave
                if os.path.exists(file):
                    os.remove(file)

            except (Exception) as ex:
                errors.append("{}".format(ex))

        if not len(errors): return None

        message = "<h2>Can not remove files:</h2> <p>{}</p><br/>".format("<br/>".join(errors))
        MessageBox.question(window, 'Can not remove files', message, MessageBox.Ok)
