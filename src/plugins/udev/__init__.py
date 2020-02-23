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
from string import Template


class Loader(object):

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def enabled(self):
        return True

    @inject.params(storage='storage')
    def boot(self, options=None, args=None, storage=None):

        storage.dispatch({
            'type': '@@app/exporter/performance/udev',
            'action': self.performance
        })

        storage.dispatch({
            'type': '@@app/exporter/powersave/udev',
            'action': self.powersave
        })

        storage.dispatch({
            'type': '@@app/exporter/cleanup/udev',
            'action': self.cleanup
        })

    @inject.params(config='config', storage='storage')
    def performance(self, config=None, storage=None):

        content = ""
        with open('templates/udev.tpl', 'r') as stream:
            template = Template(stream.read())
            if template is None: return (None, None)

            state = storage.get_state()
            if state is None: return (None, None)

            for method in state.cleanup:
                if method is None: continue

                (performance, powersave) = method()
                if performance is None: continue
                if performance.find('.rules') != -1: continue

                content += "{}\n".format(template.substitute(
                    script=performance, online=1
                ))

            return ('/etc/udev/rules.d/70-performance.rules', content)

        return (None, None)

    @inject.params(config='config', storage='storage')
    def powersave(self, config=None, storage=None):

        content = ""
        with open('templates/udev.tpl', 'r') as stream:
            template = Template(stream.read())
            if template is None: return (None, None)

            state = storage.get_state()
            if state is None: return (None, None)

            for method in state.cleanup:
                if method is None: continue

                (performance, powersave) = method()
                if powersave is None: continue

                if powersave.find('.rules') != -1: continue

                content += "{}\n".format(template.substitute(
                    script=powersave, online=0
                ))

            return ('/etc/udev/rules.d/70-powersave.rules', content)

        return (None, None)

    @inject.params(config='config')
    def cleanup(self, config=None):
        return ('/etc/udev/rules.d/70-performance.rules',
                '/etc/udev/rules.d/70-powersave.rules')


module = Loader()
