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


class SingleShot(object):

    @inject.params(storage='storage')
    def script_apply(self, single_shot=None, storage=None):

        state = storage.get_state()
        if state is None: return None

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        errors = []

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")
            for callback_performance, callback_powersave in zip(state.performance, state.powersave):

                try:

                    origin, content = callback_performance()
                    if origin is None: continue

                    file = "{}{}".format(os.path.dirname(single_shot), origin)
                    if not self._write_file(file, content):
                        raise Exception('Can not write file: {}'.format(file))

                    shell = "mkdir -p {}".format(os.path.dirname(origin))
                    stream_temp.write("{}\n".format(shell))

                    shell = "mv --force {} {}".format(file, origin)
                    stream_temp.write("{}\n\n".format(shell))

                    origin, content = callback_powersave()
                    if origin is None: continue

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

            return (single_shot, errors)

        return (None, None)

    @inject.params(storage='storage')
    def script_performance(self, single_shot=None, storage=None):

        state = storage.get_state()
        if state is None: return None

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        errors = []

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")
            for callback_performance in state.performance:

                try:

                    origin, content = callback_performance()
                    if origin is None: continue

                    file = "{}{}".format(os.path.dirname(single_shot), origin)
                    if not self._write_file(file, content):
                        raise Exception('Can not write file: {}'.format(file))

                    stream_temp.write("{}\n".format(file))

                except Exception as ex:
                    errors.append("{}".format(ex))
            stream_temp.close()

            return (single_shot, errors)

        return (None, None)

    @inject.params(storage='storage')
    def script_powersave(self, single_shot=None, storage=None):

        state = storage.get_state()
        if state is None: return None

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        errors = []
        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            for callback_powersave in state.powersave:

                try:
                    origin, content = callback_powersave()
                    if origin is None: continue

                    file = "{}{}".format(os.path.dirname(single_shot), origin)
                    if not self._write_file(file, content):
                        raise Exception('Can not write file: {}'.format(file))

                    stream_temp.write("{}\n".format(file))

                except Exception as ex:
                    errors.append("{}".format(ex))
            stream_temp.close()

            return (single_shot, errors)

        return (None, None)

    @inject.params(storage='storage')
    def script_cleanup(self, single_shot=None, storage=None):

        state = storage.get_state()
        if state is None: return None

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        errors = []

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            for callback_cleanup in state.cleanup:

                try:

                    for script in callback_cleanup():
                        if script is None: continue

                        shell = "rm -f {}".format(script)
                        stream_temp.write("{}\n".format(shell))

                except Exception as ex:
                    errors.append("{}".format(ex))

            return (single_shot, errors)

        return (None, None)

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
