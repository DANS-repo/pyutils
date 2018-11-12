#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest
from pyutils.oaipmh import id_donkey


class TestOaipmh(unittest.TestCase):

    def test_worker(self):
        id_donkey(print_worker, maxid=3, set_name=None)


def print_worker(count, dsid):
    print(count, dsid)
