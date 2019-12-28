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
import shutil

from PyQt5 import QtWidgets
from PyQt5 import QtCore

from .gui.box import MessageBox


class ModuleActions(object):

    @inject.params(config='config')
    def onActionWindowResize(self, event=None, config=None):
        config.set('window.width', '%s' % event.size().width())
        config.set('window.height', '%s' % event.size().height())
        return event.accept()

    def _write_file(self, path=None, content=None):
        if path is None or content is None:
            return None

        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        with open(path, 'w') as stream:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)
            stream.write(content)
            stream.close()
            return True
        return False

    @inject.params(window='window')
    def _dialog_script_execute(self, file=None, window=None):
        if file is None or not len(file):
            return None

        message_content = open(file, 'r').read()
        message_content = message_content.replace("\n", "<br/>")
        message = "<h2>Execute optimisation script?</h2> <p>{}</p><br/>".format(message_content)
        return MessageBox.question(window, 'Execute optimisation script?', message, MessageBox.Ok, MessageBox.Cancel)

    @inject.params(window='window')
    def _dialog_script_missed(self, message=None, window=None):
        message = "<h2>Optimisation script not found:</h2> <p>{}</p><br/>".format(message)
        return MessageBox.question(window, 'Execution script not found', message, MessageBox.Ok)

    @inject.params(window='window')
    def _dialog_script_error(self, message=None, window=None):
        message = "<h2>Can not execute optimisation script:</h2> <p>{}</p><br/>".format(message)
        return MessageBox.question(window, 'Can not execute optimisation script', message, MessageBox.Ok)

    @inject.params(window='window', container='container.exporter')
    def onActionSchemaApply(self, event=None, window=None, container=None):

        single_shot = "/tmp/performance-tuner/apply.sh"
        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        errors = []
        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")
            for exporter, priority in container.collection:
                performance, powersave = exporter.export()
                if performance is None and powersave is None:
                    continue

                try:
                    origin, content = performance

                    file = "{}{}".format(os.path.dirname(single_shot), origin)
                    if not self._write_file(file, content):
                        raise Exception('Can not write file: {}'.format(file))

                    shell = "mkdir -p {}".format(os.path.dirname(origin))
                    stream_temp.write("{}\n".format(shell))

                    shell = "mv --force {} {}".format(file, origin)
                    stream_temp.write("{}\n\n".format(shell))

                except Exception as ex:
                    errors.append("{}".format(ex))

                try:
                    origin, content = powersave

                    file = "{}{}".format(os.path.dirname(single_shot), origin)
                    if not self._write_file(file, content):
                        raise Exception('Can not write file: {}'.format(file))

                    shell = "mkdir -p {}".format(os.path.dirname(origin))
                    stream_temp.write("{}\n".format(shell))

                    shell = "mv --force {} {}".format(file, origin)
                    stream_temp.write("{}\n\n".format(shell))

                except Exception as ex:
                    errors.append("{}".format(ex))
            stream_temp.close()

        if not os.path.exists(single_shot):
            return self._dialog_script_missed(single_shot)

        if errors is not None and len(errors):
            shutil.rmtree(os.path.dirname(single_shot))
            return self._dialog_script_error("<br/>".join(errors))

        if self._dialog_script_execute(single_shot) == QtWidgets.QMessageBox.Cancel:
            return shutil.rmtree(os.path.dirname(single_shot))

        try:
            os.system('pkexec sh {} '.format(single_shot))
            return shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
        except Exception as ex:
            shutil.rmtree(os.path.dirname(single_shot))
            return self._dialog_script_error("{}".format(ex))

    @inject.params(window='window', container='container.exporter')
    def onActionSchemaCleanup(self, event=None, window=None, container=None):

        single_shot = "/tmp/performance-tuner/cleanup.sh"
        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        errors = []

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")
            for exporter, priority in container.collection:
                performance, powersave = exporter.cleanup()

                try:
                    origin, content = performance
                    shell = "rm -f {}".format(origin)
                    stream_temp.write("{}\n".format(shell))

                    origin, content = powersave
                    shell = "rm -f {}".format(origin)
                    stream_temp.write("{}\n\n".format(shell))

                except Exception as ex:
                    errors.append("{}".format(ex))

        if not os.path.exists(single_shot):
            return self._dialog_script_missed(single_shot)

        if errors is not None and len(errors):
            shutil.rmtree(os.path.dirname(single_shot))
            return self._dialog_script_error("<br/>".join(errors))

        if self._dialog_script_execute(single_shot) == QtWidgets.QMessageBox.Cancel:
            return shutil.rmtree(os.path.dirname(single_shot))

        try:
            os.system('pkexec sh {} '.format(single_shot))
            return shutil.rmtree(os.path.dirname(single_shot))
        except Exception as ex:
            shutil.rmtree(os.path.dirname(single_shot))
            return self._dialog_script_error("{}".format(ex))
