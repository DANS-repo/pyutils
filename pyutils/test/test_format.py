import unittest
import pyutils.format as fm

class TestFormat(unittest.TestCase):

    def test_link(self):
        fm.link('excel.xlsx')
