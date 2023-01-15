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
import hexdi

config = hexdi.resolve('config')
config.set('default.performance.usb', 'on')
config.set('default.performance.usb.power_level', 'on')
config.set('default.performance.usb.power_control', 'on')
config.set('default.performance.usb.autosuspend_delay', -1)
config.set('default.performance.usb.autosuspend', -1)

config.set('default.powersave.usb', 'auto')
config.set('default.powersave.usb.power_level', 'auto')
config.set('default.powersave.usb.power_control', 'auto')
config.set('default.powersave.usb.autosuspend_delay', 500)
config.set('default.powersave.usb.autosuspend', 500)
