#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
import os
from pyutils import fs


class TestFs(unittest.TestCase):

    def test_list_extensions(self):
        df = fs.list_extensions()
        print(df)

    def test_list_extensions_not_recursively(self):
        folder = '../../'
        print(os.path.abspath(folder))
        print(fs.list_extensions(folder))
        pathfilter = lambda path: os.path.abspath(path) == os.path.abspath(folder)
        df = fs.list_extensions(folder, path_filter=pathfilter)
        print('no recursion\n', df)