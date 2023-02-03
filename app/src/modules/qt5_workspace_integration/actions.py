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


@hexdi.inject('integrator.udev', 'integrator.kde', 'integrator.gnome')
def onActonApply(event, udev, kde, gnome):
    try:
        udev.integrate()
    except Exception as ex:
        print(ex)

    try:
        kde.integrate()
    except Exception as ex:
        print(ex)

    try:
        gnome.integrate()
    except Exception as ex:
        print(ex)


@hexdi.inject('config')
def onActonToggleKDE(event, config):
    config.set('kde.enabled', 1 if event else 0)


@hexdi.inject('config')
def onActonToggleGnome(event, config):
    config.set('gnome.enabled', 1 if event else 0)


@hexdi.inject('config')
def onActonToggleXfce(event, config):
    config.set('xfce.enabled', 1 if event else 0)


@hexdi.inject('config')
def onActonToggleDeepin(event, config):
    config.set('deepin.enabled', 1 if event else 0)


@hexdi.inject('config')
def onActonToggleCinnamon(event, config):
    config.set('cinnamon.enabled', 1 if event else 0)


@hexdi.inject('config')
def onActonToggleBudgie(event, config):
    config.set('budgie.enabled', 1 if event else 0)


@hexdi.inject('config')
def onActonToggleUdev(event, config):
    config.set('udev.enabled', 1 if event else 0)
