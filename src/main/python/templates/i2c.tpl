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
source = '/sys/bus/i2c/devices'
if not os.path.exists(source): sys.exit()

for device in glob.glob('{}/i2c-*'.format(source)):
    if device in ignored:
        continue

    power_control = '{}/power/control'.format(device)
    if not os.path.exists(power_control): continue
    with open(power_control, 'w', errors='ignore') as stream:
        stream.write('$schema')
