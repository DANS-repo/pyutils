#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from pyutils import fs


class TestFs(unittest.TestCase):

    def test_list_extensions(self):
        df = fs.list_extensions()
        print(df)