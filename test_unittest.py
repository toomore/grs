# -*- coding: utf-8 -*-
''' Unittest '''
import grs
import unittest
from datetime import datetime
from types import BooleanType
from types import NoneType


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
        assert result == self.data.MA(3)

    def test_moving_average_value(self):
        self.get_data()
        result = self.data.moving_average_value(3)
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)
        assert result == self.data.MAV(3)

    def test_moving_average_bias_ratio(self):
        self.get_data()
        result = self.data.moving_average_bias_ratio(6, 3)
        assert isinstance(result[0], list)
        assert isinstance(result[1], int)
        assert result == self.data.MAO(6, 3)

    def test_check_moving_average_bias_ratio(self):
        self.get_data()
        param = (self.data.moving_average_bias_ratio(6, 3)[0], True)
        result = self.data.check_moving_average_bias_ratio(*param)[0]
        assert isinstance(result, BooleanType)
        assert result == self.data.CKMAO(*param)[0]

    def test_CKMAO_classmethod(self):
        self.get_data()
        result = grs.fetch_data.SimpleAnalytics.CKMAO(self.data.MAO(3, 6)[0])
        assert isinstance(result, tuple)
        assert len(result) == 3

    def test_stock_value(self):
        self.get_data()
        assert isinstance(self.data.price, list)
        assert isinstance(self.data.openprice, list)
        assert isinstance(self.data.value, list)

    @staticmethod
    def test_twse_no():
        twse_no = grs.TWSENo()
        assert isinstance(twse_no.all_stock, dict)
        result = twse_no.search(u'中')
        # 1701 中化
        assert '1701' in result
        result = twse_no.searchbyno(17)
        assert '1701' in result

    @staticmethod
    def test_twse_code_comps():
        twseno = grs.TWSENo()
        industry_code = twseno.industry_code
        industry_comps = twseno.industry_comps
        for i in industry_comps:
            assert i in industry_code

    @staticmethod
    def test_twse_open():
        is_open = grs.TWSEOpen()
        result = is_open.d_day(datetime(2014, 1, 1))
        assert result is False

    @staticmethod
    @unittest.skip('Known issues.')
    def test_realtime():
        real_time = grs.RealtimeStock('2618')
        assert real_time.real['no'] == '2618'
        real_time = grs.RealtimeWeight()
        assert real_time.real['no'] == '1'
        real_time = grs.RealtimeStock('0050')
        assert real_time.real['no'] == '0050'
        try:
            real_time = grs.RealtimeStock(0050)
        except AssertionError:
            pass

    @staticmethod
    def test_countdown():
        result = grs.Countdown().countdown
        assert isinstance(result, int)

    @staticmethod
    def test_taiwan_50():
        stock = grs.Stock('0050')
        assert u'台灣50' == stock.info[1]
        try:
            stock = grs.Stock(0050)
        except AssertionError:
            pass

class TestGrsOTC(unittest.TestCase):
    def get_data(self):
        self.stock_no = '8446'
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

    @staticmethod
    def test_otc_no():
        otc_no = grs.OTCNo()
        assert isinstance(otc_no.all_stock, dict)
        result = otc_no.search(u'華')
        # 8446 華研
        assert '8446' in result
        result = otc_no.searchbyno(46)
        assert '8446' in result

    @staticmethod
    def test_otc_code_comps():
        twseno = grs.OTCNo()
        industry_code = twseno.industry_code
        industry_comps = twseno.industry_comps
        for i in industry_comps:
            assert i in industry_code


if __name__ == '__main__':
    unittest.main()
