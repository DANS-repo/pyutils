#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class ListCollector(object):

    def __init__(self, repeater=None):
        self.__repeater = repeater
        self.__coll = {}
        self.__row = -1
        self.__max = -1

    def add(self, name, list_):
        self.__coll[name] = list_

    def max_len(self):
        mk = None
        ml = 0
        for k, v in self.__coll.items():
            l = len(v)
            if l >= ml:
                mk = k
                ml = l
        return mk, ml

    def start_iter(self):
        self.__row = -1
        mk, ml = self.max_len()
        self.__max = ml

    def has_next(self):
        self.__row += 1
        return self.__row < self.__max

    def next(self, key):
        if self.__row >= len(self.__coll[key]):
            return ''
        else:
            return self.__coll[key][self.__row]

    def next_row(self):
        row = []
        if self.__repeater:
            row.append(self.__repeater)
        for key in self.__coll.keys():
            row.append(self.next(key))
        return row