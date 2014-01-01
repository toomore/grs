# -*- coding: utf-8 -*-
''' Unittest '''
from datetime import datetime
from types import BooleanType
from types import NoneType
import grs
import unittest


class TestGrs(unittest.TestCase):
    def get_data(self):
        self.stock_no = '2618'
        self.data = grs.Stock(self.stock_no)

    def test_stock(self):
        self.get_data()
        assert self.data.info[0] == self.stock_no

    def test_best_buy_or_sell(self):
        self.get_data()
        assert isinstance(grs.BestFourPoint(self.data).best_four_point(),
                          (tuple, NoneType))

    def test_moving_average(self):
        self.get_data()
        result = self.data.moving_average(3)
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)

    def test_moving_average_value(self):
        self.get_data()
        result = self.data.moving_average_value(3)
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)

    def test_moving_average_bias_ratio(self):
        self.get_data()
        result = self.data.moving_average_bias_ratio(6, 3)
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)

    def test_check_moving_average_bias_ratio(self):
        self.get_data()
        result = self.data.check_moving_average_bias_ratio(
                               self.data.moving_average_bias_ratio(3, 6)[0],
                               positive_or_negative=True)[0]
        assert isinstance(result, BooleanType)

    def test_stock_value(self):
        self.get_data()
        assert isinstance(self.data.price, list)
        assert isinstance(self.data.openprice, list)
        assert isinstance(self.data.value, list)

    def test_twse_no(self):
        twse_no = grs.TWSENo()
        assert isinstance(twse_no.all_stock, dict)
        result = twse_no.search(u'中')
        # 1701 中化
        assert 1701 in result
        result = twse_no.searchbyno(17)
        assert 1701 in result

    def test_twse_open(self):
        is_open = grs.TWSEOpen()
        result = is_open.d_day(datetime(2014, 1, 1))
        assert result is False

    def test_realtime(self):
        real_time = grs.RealtimeStock('2618')
        assert real_time.real['no'] == '2618'
        real_time = grs.RealtimeWeight()
        assert real_time.real['no'] == '1'

    @staticmethod
    def test_countdown():
        result = grs.Countdown().countdown
        assert isinstance(result, int)

if __name__ == '__main__':
    unittest.main()
