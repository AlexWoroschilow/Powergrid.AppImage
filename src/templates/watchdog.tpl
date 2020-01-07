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

source = '/proc/sys/kernel/nmi_watchdog'
if not os.path.exists(source): sys.exit()
# (On older kernels you may need to use noatime instead of relatime.)
# Also consider merely using a larger value for the commit option. This defines how often changed data is written to the disk (it is cached until then).
# The default value is 5 seconds.
# See man mount(8) for details on how the rel/noatime and commit options work.
# Use laptop_mode to reduce disk usage by delaying and grouping writes. You should enable it, at least while on battery.
with open(source, 'w', errors='ignore') as stream:
    stream.write('$schema')
