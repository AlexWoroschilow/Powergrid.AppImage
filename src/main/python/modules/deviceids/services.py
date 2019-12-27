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
import configparser
import mmap
import re
import contextlib


class DeviceLocator(object):

    def __init__(self, file=None):
        self.file = file

    def __call__(self, *args, **kwargs):
        return self

    def get(self, vendor, product):
        with open(self.file, 'rb', 0) as file, mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as stream:

            vendor_byte = "\n{}".format(vendor)
            vendor_byte = vendor_byte.encode('utf-8')
            vposition = stream.find(vendor_byte)
            if vposition == -1:
                return None

            stream.seek(vposition + 1)
            name_vendor = stream.readline()
            name_vendor = name_vendor.decode('utf-8')
            name_vendor = name_vendor.strip("\n{}\t".format(vendor))
            name_vendor = name_vendor.strip(" \n")

            product_byte = "\t{}".format(product)
            product_byte = product_byte.encode('utf-8')
            pposition = stream.find(product_byte)
            if pposition == -1:
                return name_vendor

            stream.seek(pposition)
            name_product = stream.readline()
            name_product = name_product.decode('utf-8')
            name_product = name_product.strip("\n{}\t".format(product))
            name_product = name_product.strip(" \n")

            return name_product

        return "{}:{}".format(vendor, product)
