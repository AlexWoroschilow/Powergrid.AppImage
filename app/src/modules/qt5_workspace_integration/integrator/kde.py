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
import mmap
import os

import hexdi


@hexdi.permanent('integrator.kde')
class KdeIntegrator(object):
    settings = [
        [
            "[AC][RunScript]\n",
            "scriptCommand={}\n".format(os.path.expanduser("~/.local/PerformanceTuner/performance.sh")),
            "scriptPhase=0\n"
        ],
        [
            "[Battery][RunScript]\n",
            "scriptCommand={}\n".format(os.path.expanduser("~/.local/PerformanceTuner/powersave.sh")),
            "scriptPhase=0\n"
        ],
        [
            "[LowBattery][RunScript]\n",
            "scriptCommand={}\n".format(os.path.expanduser("~/.local/PerformanceTuner/powersave.sh")),
            "scriptPhase=0\n"
        ]
    ]

    @hexdi.inject('config', 'udev_dumper.performance', 'udev_dumper.powersave')
    def integrate(self, config=None, performance=None, powersave=None):
        integration = '~/.local/PerformanceTuner'
        performance.dump(os.path.expanduser("{}/performance.sh".format(integration)))
        powersave.dump(os.path.expanduser("{}/powersave.sh".format(integration)))

        kdefile = os.path.expanduser("~/.config/powermanagementprofilesrc")
        if not os.path.exists(os.path.dirname(kdefile)): return self

        if config.has('kde.enabled') and int(config.get('kde.enabled')):
            with open(kdefile, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
                if s.find(b'PerformanceTuner/kde/performance.sh') != -1 and s.find(b'PerformanceTuner/kde/powersave.sh') != -1:
                    return self

            with open(kdefile, 'a') as stream:
                for config in self.settings:
                    for line in config:
                        stream.write("{}".format(line))
                stream.close()

            return self

        with open(kdefile, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as s:
            if s.find(b'PerformanceTuner/kde/performance.sh') == -1 and s.find(b'PerformanceTuner/kde/powersave.sh') == -1:
                return self

        with open(kdefile, 'r') as stream:
            content = stream.read()
            stream.close()

            for config in self.settings:
                for line in config:
                    content = content.replace(line, '')

            with open(kdefile, 'w') as stream:
                stream.write(content)
                stream.close()
