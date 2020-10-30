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

import hexdi


class DumperSchema(object):

    @hexdi.inject('udev_rules.performance', 'udev_rules.powersave')
    def dump(self, single_shot, performance, powersave):

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            os.chmod(single_shot, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)

            stream_temp.write("echo '#' > /etc/udev/rules.d/70-performance.rules\n")
            stream_temp.write("echo '# DO NOT EDIT THIS FILE' >> /etc/udev/rules.d/70-performance.rules\n")
            stream_temp.write("echo '#' >> /etc/udev/rules.d/70-performance.rules\n")
            stream_temp.write("echo '# It is automatically generated' >> /etc/udev/rules.d/70-performance.rules\n")
            stream_temp.write("echo '#' >> /etc/udev/rules.d/70-performance.rules\n")

            for rule in performance.rules:
                stream_temp.write("echo '{}' >> /etc/udev/rules.d/70-performance.rules\n".format(rule))

            for rule in powersave.rules:
                stream_temp.write("echo '{}' >> /etc/udev/rules.d/70-performance.rules\n".format(rule))

            stream_temp.write("chmod 644 /etc/udev/rules.d/70-performance.rules\n")

            stream_temp.close()
            return single_shot

        return None


class DumperCleaner(object):

    def dump(self, single_shot):
        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            os.chmod(single_shot, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)

            stream_temp.write("rm -f /etc/udev/rules.d/70-performance.rules\n")

            stream_temp.close()
            return single_shot

        return None


class DumperExport(object):

    @hexdi.inject('udev_rules.performance', 'udev_rules.powersave')
    def dump(self, single_shot, performance, powersave):

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:

            os.chmod(single_shot, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)

            for rule in performance.rules:
                stream_temp.write("{}\n".format(rule))

            for rule in powersave.rules:
                stream_temp.write("{}\n".format(rule))

            stream_temp.close()
            return single_shot

        return None


class DumperPerformance(object):

    @hexdi.inject('rules.performance')
    def dump(self, single_shot, performance):

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            os.chmod(single_shot, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)

            for rule in performance.rules:
                stream_temp.write("{}\n".format(rule))

            stream_temp.close()
            return single_shot

        return None


class DumperPowersave(object):

    @hexdi.inject('rules.powersave')
    def dump(self, single_shot, performance):

        if not os.path.exists(os.path.dirname(single_shot)):
            os.makedirs(os.path.dirname(single_shot), exist_ok=True)

        with open(single_shot, 'w') as stream_temp:
            stream_temp.write("#! /bin/sh\n\n")

            os.chmod(single_shot, stat.S_IRUSR | stat.S_IWUSR |
                     stat.S_IXUSR | stat.S_IXGRP | stat.S_IRGRP |
                     stat.S_IXOTH | stat.S_IROTH)

            for rule in performance.rules:
                stream_temp.write("{}\n".format(rule))

            stream_temp.close()
            return single_shot

        return None
