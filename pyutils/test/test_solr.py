import unittest
import pyutils.solr as solr


class TestSolr(unittest.TestCase):

    def test_search(self):
        print(solr.search('emd_audience:"easy-discipline:2"'))