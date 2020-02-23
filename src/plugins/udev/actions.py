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

from string import Template

from PyQt5 import QtWidgets
from .gui.box import MessageBox


class ModuleActions(object):
    path = '/etc/udev/rules.d/70-performance.rules'

    @inject.params(container='container.exporter')
    def _write_file(self, path, container=None):

        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        with open(path, 'w') as stream:
            os.chmod(path, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)

            template = Template(open('templates/udev.tpl', 'r').read())
            for exporter, priority in container.collection:
                (performance_name, content), (powersave_name, content) = exporter.cleanup()
                if performance_name is None or powersave_name is None:
                    continue

                stream.write(template.substitute(
                    performance=performance_name,
                    powersave=powersave_name
                ))
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
        result = MessageBox(window, 'Execute optimisation script?', message, MessageBox.Ok, MessageBox.Cancel)
        return result.exec_()

    @inject.params(window='window')
    def _dialog_script_missed(self, message=None, window=None):
        message = "<h2>Optimisation script not found:</h2> <p>{}</p><br/>".format(message)
        return MessageBox.question(window, 'Execution script not found', message, MessageBox.Ok)

    @inject.params(window='window')
    def _dialog_script_error(self, message=None, window=None):
        message = "<h2>Can not execute optimisation script:</h2> <p>{}</p><br/>".format(message)
        return MessageBox.question(window, 'Can not execute optimisation script', message, MessageBox.Ok)

    @inject.params(window='window')
    def onActionSchemaApply(self, event=None, window=None):

        single_shot = "/tmp/performance-tuner/apply.sh"
        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            file = "{}{}".format(os.path.dirname(single_shot), self.path)
            if not len(file) or not self._write_file(file):
                raise Exception('Can not write file: {}'.format(file))

            shell = "mkdir -p {}".format(os.path.dirname(self.path))
            stream_temp.write("{}\n".format(shell))

            shell = "mv --force {} {}".format(file, self.path)
            stream_temp.write("{}\n\n".format(shell))

            stream_temp.close()

        if not os.path.exists(single_shot):
            return self._dialog_script_missed(single_shot)

        if self._dialog_script_execute(single_shot) == QtWidgets.QMessageBox.Cancel:
            shutil.rmtree(os.path.dirname(single_shot))
            return None

        try:
            os.system('pkexec sh {} '.format(single_shot))
            shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)

        except Exception as ex:
            shutil.rmtree(os.path.dirname(single_shot), ignore_errors=True)
            return self._dialog_script_error("{}".format(ex))

    @inject.params(window='window', exporter='container.exporter')
    def onActionSchemaCleanup(self, event=None, window=None, exporter=None):

        single_shot = "/tmp/performance-tuner/apply.sh"
        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")
            stream_temp.write("rm -f {}\n".format(self.path))
            stream_temp.close()

        if not os.path.exists(single_shot):
            return self._dialog_script_missed(single_shot)

        if self._dialog_script_execute(single_shot) == QtWidgets.QMessageBox.Cancel:
            shutil.rmtree(os.path.dirname(single_shot))
            return None

        try:
            os.system('pkexec sh {} '.format(single_shot))
            shutil.rmtree(os.path.dirname(single_shot))
        except Exception as ex:
            shutil.rmtree(os.path.dirname(single_shot))
            return self._dialog_script_error("{}".format(ex))
