# -*- coding: utf-8 -*-
''' Unittest '''
import grs
import unittest


class TestGrs(unittest.TestCase):
    def setUp(self):
        self.data = grs.stock(2618)

    def test_stock(self):
        assert self.data.info[0] == '2618'

if __name__ == '__main__':
    unittest.main()
