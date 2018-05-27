#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import unittest

from pyutils.collect import ListCollector


class TestCollect(unittest.TestCase):

    def test_collect(self):
        ls = ListCollector()
        ls.add('alpha', ['a', 'b', 'c'])
        ls.add('beta', ['d', 'e'])
        ls.add('gamma', [])
        ls.add('nogw', ['x', 'y'])

        key, max_ = ls.max_len()
        self.assertEqual(key, 'alpha')
        self.assertEqual(max_, 3)

        ls.start_iter()
        while ls.has_next():
            print(ls.next_row())

    def test_repeater(self):
        ls = ListCollector('repeat this')
        ls.add('alpha', ['a', 'b', 'c'])
        ls.add('beta', ['d', 'e'])
        ls.add('gamma', [])
        ls.add('nogw', ['x', 'y'])

        ls.start_iter()
        while ls.has_next():
            print(ls.next_row())

    def test_failure(self):
        lc = ListCollector()
        with self.assertRaises(RuntimeError):
            lc.add('foo', lc)