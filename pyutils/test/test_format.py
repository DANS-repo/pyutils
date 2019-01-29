import unittest
import pyutils.format as fm


class TestFormat(unittest.TestCase):

    def test_link_directory(self):
        fm.link('test_format.py')

    def test_messages(self):
        fm.messages()

    def test_format_size(self):
        print(fm.format_size(1))
        print(fm.format_size(100))
        print(fm.format_size(10000))
        print(fm.format_size(1000000))
        print(fm.format_size(100000000))
        print(fm.format_size(10000000000))
        print(fm.format_size(1024))
        print(fm.format_size(1024 * 1024))
        print(fm.format_size(1024 * 1024 * 1024, trailing=5))
        print(fm.format_size(1024 * 1024 * 1024, leading=-1, trailing=2))


