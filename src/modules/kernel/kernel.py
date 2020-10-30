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
import glob
import logging
import os
from importlib import util


class Kernel(object):

    def __init__(self, options: {} = None, args: [] = None, sources: [] = ["plugins/**", "modules/**"]):

        self.modules = self._modules(
            sources, options, args
        )

        logger = logging.getLogger('kernel')
        for module in self.modules:
            spec = util.find_spec('{}.interface'.format(module.__name__))
            logger.debug("booting: {}".format(module))
            if spec and spec.loader: spec.loader.load_module()

    def _candidates(self, sources: [] = None):
        for mask in sources:
            if not mask:
                continue

            for source in glob.glob(mask):
                if not source:
                    continue

                if not os.path.isdir(source):
                    continue

                yield source.replace('/', '.')

    def _modules(self, sources: [] = None, options: {} = None, args: [] = None):

        modules = []

        logger = logging.getLogger('kernel')
        for source in self._candidates(sources):
            try:

                spec = util.find_spec(source)
                if not spec.loader: continue

                module = spec.loader.load_module()
                if not module: continue
                logger.debug("found: {}".format(source))

                if hasattr(module, 'enabled') and callable(module, 'enabled'):
                    enabled = getattr(module, 'enabled')
                    if not enabled(options, args):
                        continue

                logger.debug("loading: {}".format(module))
                modules.append(module)

            except (SyntaxError, RuntimeError) as err:
                logger.critical("{}: {}".format(source, err))
                continue

        return modules
