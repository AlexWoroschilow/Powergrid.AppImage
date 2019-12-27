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
import glob
import hexdi
import logging
import importlib
import functools


class Kernel(object):

    def __init__(self, options=None, args=None, sources=["modules/**/__init__.py", "plugins/**/__init__.py"]):

        container = hexdi.get_root_container()
        container.bind_type(self, 'kernel', hexdi.lifetime.PermanentLifeTimeManager)

        self.modules = self.get_modules(sources)

        logger = logging.getLogger('kernel')
        for module in self.modules:
            if not hasattr(module, 'boot'): continue

            loader_boot = getattr(module, 'boot')
            if not callable(loader_boot): continue

            logger.debug("booting: {}".format(module))
            module.boot(options, args)

    def __call__(self, *args, **kwargs):
        return self

    @staticmethod
    def get_module_candidates(sources=None):
        for mask in sources:
            for source in glob.glob(mask):
                if not os.path.exists(source):
                    continue

                yield source.replace('/', '.') \
                    .replace('.py', '')

    def get_modules(self, sources=None):

        modules = []

        logger = logging.getLogger('kernel')
        for source in self.get_module_candidates(sources):
            try:

                module = importlib.import_module(source, False)
                logger.debug("found: {}".format(source))

                with module.module as loader:
                    if hasattr(loader, 'enabled'):
                        if not loader.enabled:
                            continue

                    logger.debug("loading: {}".format(source))

                    modules.append(loader)

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(source, err))
                continue

        return modules

    def configure(self, binder, modules, options=None, args=None):

        logger = logging.getLogger('kernel')
        for module in modules:

            try:

                if not hasattr(module, 'configure'):
                    continue

                configure = getattr(module, 'configure')
                if not callable(configure):
                    continue

                logger.debug("configuring: {}".format(module))

                binder.install(functools.partial(
                    module.configure,
                    options=options,
                    args=args
                ))

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(module, err))
                continue

        binder.bind('kernel', self)

    def get(self, name=None):
        container = inject.get_injector()
        return container.get_instance(name)
