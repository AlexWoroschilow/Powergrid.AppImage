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

if not config.has('udev.enabled'): config.set('udev.enabled', 1)
if not config.has('gnome.enabled'): config.set('gnome.enabled', 0)
if not config.has('kde.enabled'): config.set('kde.enabled', 0)
if not config.has('xfce.enabled'): config.set('xfce.enabled', 0)
if not config.has('deepin.enabled'): config.set('deepin.enabled', 0)
if not config.has('cinnamon.enabled'): config.set('cinnamon.enabled', 0)
if not config.has('budgie.enabled'): config.set('budgie.enabled', 0)
