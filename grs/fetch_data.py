# -*- coding: utf-8 -*-
'''' Fetch data from TWSE '''
# Copyright (c) 2012, 2013, 2014 Toomore Chiang, http://toomore.net/
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
import logging
import random
import urllib2

class Stock(object):
    """ 擷取股票股價 """

    def __init__(self, stock_no, mons=3):
        """ 擷取股票股價

            :param str stock_no: 股價代碼
            :param int mons: 擷取近 n 個月的資料
            :return: grs.Stock
        """
        assert isinstance(stock_no, str), '`stock_no` must be a string'
        self.__get_mons = 0
        self.__get_no = 0
        self.__info = ()
        self.__raw_rows_name = []
        self.__url = []
        self.__raw_data = self.__serial_fetch(stock_no, mons)

    @property
    def url(self):
        """ 擷取資料網址

            :rtype: list
            :returns: url in list
        """

        return self.__url

    @property
    def info(self):
        """ (股票代碼, 股票名稱)

            :rtype: tuple
            :returns: (股票代碼, 股票名稱)
        """
        return self.__info

    @property
    def raw(self):
        """ 擷取原始檔案

            :rtype: list
            :returns: data in list
        """
        return self.__raw_data

    def get_raw_rows(self, rows=6):
        """ 取出某一價格序列 *(舊→新)*

            預設序列收盤價 *(self.__serial_price(6))*

            :rtype: list
            :returns: 預設序列收盤價 *(self.__serial_price(6))*
        """
        return self.__serial_price(rows)

    @property
    def get_raw_rows_name(self):
        """ 原始檔案的欄位名稱

            0. 日期
            1. 成交股數
            2. 成交金額
            3. 開盤價
            4. 最高價（續）
            5. 最低價
            6. 收盤價
            7. 漲跌價差
            8. 成交筆數

            :rtype: list
        """
        result = [i.decode('cp950') for i in self.__raw_rows_name]
        return result

    def __fetch_data(self, stock_no, nowdatetime):
        """ Fetch data from twse.com.tw
            return list.
            從 twse.com.tw 下載資料，回傳格式為 csv.reader

            0. 日期
            1. 成交股數
            2. 成交金額
            3. 開盤價
            4. 最高價（續）
            5. 最低價
            6. 收盤價
            7. 漲跌價差
            8. 成交筆數

            :param str stock_no: 股票代碼
            :param datetime nowdatetime: 此刻時間
            :rtype: list
        """
        url = (
            'http://www.twse.com.tw/ch/trading/exchange/' +
            'STOCK_DAY/STOCK_DAY_print.php?genpage=genpage/' +
            'Report%(year)d%(mon)02d/%(year)d%(mon)02d_F3_1_8_%(stock)s.php' +
            '&type=csv&r=%(rand)s') % {'year': nowdatetime.year,
                                       'mon': nowdatetime.month,
                                       'stock': stock_no,
                                       'rand': random.randrange(1, 1000000)}
        logging.info(url)
        csv_read = csv.reader(urllib2.urlopen(url).readlines())
        self.__url.append(url)
        return csv_read

    def __to_list(self, csv_file):
        """ 串接每日資料 舊→新

            :param csv csv_file: csv files
            :rtype: list
        """
        tolist = []
        for i in csv_file:
            i = [value.strip().replace(',', '') for value in i]
            try:
                for value in (1, 2, 3, 4, 5, 6, 8):
                    i[value] = float(i[value])
            except (IndexError, ValueError):
                pass
            tolist.append(i)
        if len(tolist):
            self.__info = (tolist[0][0].split(' ')[1],
                           tolist[0][0].split(' ')[2].decode('cp950'))
            self.__raw_rows_name = tolist[1]
            return tuple(tolist[2:])
        else:
            return tuple([])

    def __serial_fetch(self, stock_no, month):
        """ 串接每月資料 舊→新

            :param str stock_no: 股票代碼
            :param int month: 擷取 n 個月的資料
            :rtype: tuple
        """
        result = ()
        self.__get_mons = month
        self.__get_no = stock_no
        for i in range(month):
            nowdatetime = datetime.today() - relativedelta(months=i)
            tolist = self.__to_list(self.__fetch_data(stock_no, nowdatetime))
            result = tolist + result
        return tuple(result)

    def __plus_mons(self, month):
        """ 增加 n 個月的資料

            :param int month: 增加 n 個月的資料
            :rtype: tuple
        """
        result = []
        exist_mons = self.__get_mons
        oldraw = list(self.__raw_data)
        for i in range(month):
            nowdatetime = datetime.today() - relativedelta(months=exist_mons) -\
                          relativedelta(months=i)
            tolist = self.__to_list(
                                self.__fetch_data(self.__info[0], nowdatetime))
            result = list(tolist) + result
        result = result + oldraw
        self.__get_mons = exist_mons + month
        return tuple(result)

    def plus_mons(self, month):
        """ 新增擴充月份資料

            :param int month: 增加 n 個月的資料
        """
        self.__raw_data = self.__plus_mons(month)

    def out_putfile(self, fpath):
        """ 輸出成 CSV 檔

            :param path fpath: 檔案輸出位置

            .. todo:: files output using `with` syntax.
        """
        with open(fpath, 'w') as csv_file:
            output = csv.writer(csv_file)
            output.writerows(self.__raw_data)

    def __serial_price(self, rows=6):
        """ 取出某一價格序列 *(舊→新)*

            預設序列收盤價 *(self.__serial_price(6))*

            :rtype: list
            :returns: 預設序列收盤價 *(self.__serial_price(6))*
        """
        result = (float(i[rows]) for i in self.__raw_data)
        return list(result)

    def __calculate_moving_average(self, date, row):
        """ 計算移動平均數

            :param int row: 收盤價(6)、成交股數(1)
            :rtype: tuple (序列 舊→新, 持續天數)
        """
        cal_data = self.__serial_price(row)
        result = []
        for dummy in range(len(cal_data) - int(date) + 1):
            result.append(round(sum(cal_data[-date:]) / date, 2))
            cal_data.pop()
        result.reverse()
        cont = self.__cal_continue(result)
        return result, cont

    @classmethod
    def __cal_continue(cls, list_data):
        """ 計算持續天數

            :rtype: int
            :returns: 向量數值：正數向上、負數向下。
        """
        diff_data = []
        for i in range(1, len(list_data)):
            if list_data[-i] > list_data[-i - 1]:
                diff_data.append(1)
            else:
                diff_data.append(-1)
        cont = 0
        for value in diff_data:
            if value == diff_data[0]:
                cont += 1
            else:
                break
        return cont * diff_data[0]

    def moving_average(self, date):
        """ 計算 n 日收盤均價與持續天數

            :param int date: n 日
            :rtype: tuple (序列 舊→新, 持續天數)
        """
        return self.__calculate_moving_average(date, 6)

    def moving_average_value(self, date):
        """ 計算 n 日成交股數均量與持續天數

            :param int date: n 日
            :rtype: tuple (序列 舊→新, 持續天數)
        """
        val, conti = self.__calculate_moving_average(date, 1)
        val = (round(i / 1000, 3) for i in val)
        return list(val), conti

    def moving_average_bias_ratio(self, date1, date2):
        """ 計算乖離率（均價）
            date1 - date2

            :param int data1: n 日
            :param int data2: m 日
            :rtype: tuple (序列 舊→新, 持續天數)
        """
        data1 = self.moving_average(date1)[0]
        data2 = self.moving_average(date2)[0]
        cal_list = []
        for i in range(1, min(len(data1), len(data2)) + 1):
            cal_list.append(data1[-i] - data2[-i])
        cal_list.reverse()
        cont = self.__cal_continue(cal_list)
        return cal_list, cont

    @property
    def price(self):
        """ 收盤價股價序列

            :rtype: list
        """
        return self.__serial_price()

    @property
    def openprice(self):
        """ 開盤價股價序列

            :rtype: list
        """
        return self.__serial_price(3)

    @property
    def value(self):
        """ 成交量序列

            :rtype: list
        """
        val = (round(i / 1000, 3) for i in self.__serial_price(1))
        return list(val)

    @classmethod
    def __cal_ma_bias_ratio_point(cls, data, sample=5,
                                  positive_or_negative=False):
        """判斷轉折點位置

           :param list data: 計算資料
           :param int sample: 計算的區間樣本數量
           :param bool positive_or_negative: 正乖離 為 True，負乖離 為 False
           :rtype: tuple
           :returns: (True or False, 第幾個轉折日, 轉折點值)
        """
        sample_data = data[-sample:]
        if positive_or_negative:  # 正
            ckvalue = max(sample_data)  # 尋找最大值
            preckvalue = max(sample_data) > 0  # 區間最大值必須為正
        else:
            ckvalue = min(sample_data)  # 尋找最小值
            preckvalue = max(sample_data) < 0  # 區間最大值必須為負
        return (sample - sample_data.index(ckvalue) < 4 and \
                sample_data.index(ckvalue) != sample - 1 and preckvalue,
                sample - sample_data.index(ckvalue) - 1,
                ckvalue)

    def check_moving_average_bias_ratio(self, data, sample=5,
                                        positive_or_negative=False):
        """判斷正負乖離轉折點位置

           :param list data: 計算資料
           :param int sample: 計算的區間樣本數量
           :param bool positive_or_negative: 正乖離 為 True，負乖離 為 False
           :rtype: tuple
           :returns: (True or False, 第幾個轉折日, 轉折點值)
        """
        return self.__cal_ma_bias_ratio_point(data, sample,
                                              positive_or_negative)
