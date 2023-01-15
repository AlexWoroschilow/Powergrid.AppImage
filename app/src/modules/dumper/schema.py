# Copyright 2020 Alex Woroschilow (alex.woroschilow@gmail.com)
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


class SingleShot(object):

    @hexdi.inject('udev_rules.performance', 'udev_rules.powersave')
    def script_apply(self, single_shot, performance, powersave):
        with open(single_shot, 'w') as stream_temp:
            for rule in performance.rules:
                stream_temp.write(rule)
            for rule in powersave.rules:
                stream_temp.write(rule)
            stream_temp.close()
