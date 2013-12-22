# -*- coding: utf-8 -*-
''' Unittest '''
from types import NoneType
import grs
import unittest


class TestGrs(unittest.TestCase):
    def setUp(self):
        self.stock_no = '2618'
        self.data = grs.stock(self.stock_no)

    def test_stock(self):
        assert self.data.info[0] == self.stock_no

    def test_best_buy_or_sell(self):
        assert isinstance(grs.BestFourPoint(self.data).best_four_point(),
                          (tuple, NoneType))

if __name__ == '__main__':
    unittest.main()
