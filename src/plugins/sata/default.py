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
config.set('default.performance.sata.policy', 'max_performance')
config.set('default.balanced.sata.policy', 'med_power_with_dipm')
config.set('default.powersave.sata.policy', 'min_power')
config.set('default.performance.sata.control', 'on')
config.set('default.powersave.sata.control', 'auto')
