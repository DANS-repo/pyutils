import unittest
import pyutils.format as fm


class TestFormat(unittest.TestCase):

    def test_link(self):
        fm.link('excel.xlsx')

    def test_link_directory(self):
        fm.link('../../2018/twister/data/')

    def test_messages(self):
        fm.messages()

