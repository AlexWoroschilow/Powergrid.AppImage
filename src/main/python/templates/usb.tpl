#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright 2019 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITION
import os
import sys
import glob

ignored = [$ignored]
source = '/sys/bus/usb/devices'
if not os.path.exists(source): sys.exit()

for device in glob.glob('{}/*'.format(source)):
    if device in ignored:
        continue

    power_level = '{}/power/level'.format(device)
    if os.path.exists(power_level) and os.path.isfile(power_level):
        with open(power_level, 'w', errors='ignore') as stream:
            stream.write('$power_level')

    power_control = '{}/power/control'.format(device)
    if os.path.exists(power_control) and os.path.isfile(power_control):
        with open(power_control, 'w', errors='ignore') as stream:
            stream.write('$power_control')

    autosuspend = '{}/power/autosuspend_delay_ms'.format(device)
    if os.path.exists(autosuspend) and os.path.isfile(autosuspend):
        with open(autosuspend, 'w', errors='ignore') as stream:
            stream.write('$autosuspend_delay')

    autosuspend = '{}/power/autosuspend'.format(device)
    if os.path.exists(autosuspend) and os.path.isfile(autosuspend):
        with open(autosuspend, 'w', errors='ignore') as stream:
            stream.write('$autosuspend')
