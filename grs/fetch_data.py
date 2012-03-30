#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2012 Toomore Chiang, http://toomore.net/
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

from datetime import datetime, timedelta
import csv
import logging
import random
import urllib2


class stock(object):
    """ 擷取股票股價 """

    def __init__(self, stock_no, mons=3):
        """ 擷取股票股價
            :stock_no : 股價代碼
            :mons : 擷取近 n 個月的資料
        """
        self.__url = []
        self.__info = ()
        self.__raw_data = self.__serial_fetch(stock_no, mons)

    @property
    def url(self):
        """ [list] 擷取資料網址 """
        return self.__url

    @property
    def info(self):
        """ [tuple] (股票代碼, 股票名稱) """
        return self.__info

    @property
    def raw(self):
        """ [list] 擷取原始檔案 """
        return self.__raw_data

    def getRawRows(self, rows=6):
        """ [list] 取出某一價格序列 舊→新
            預設序列收盤價 → __serial_price(6)
        """
        return self.__serial_price(rows)

    @property
    def getRawRowsName(self):
        """ 原始檔案的欄位名稱 """
        re = [i.decode('big5') for i in self.__RawRowsName]
        return re

    def __fetch_data(self, stock_no, nowdatetime=datetime.today()):
        """ Fetch data from twse.com.tw
            return list.
            從 twse.com.tw 下載資料，回傳格式為 csv.reader
            欄位：
                日期 成交股數 成交金額 開盤價 最高價 （續）
                最低價 收盤價 漲跌價差 成交筆數
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
        cc = urllib2.urlopen(url)
        cc_read = cc.readlines()
        csv_read = csv.reader(cc_read)
        self.__url.append(url)
        return csv_read

    def __to_list(self, csv_file):
        """ [list] 串接每日資料 舊→新"""
        tolist = []
        for i in csv_file:
            i = [v.strip().replace(',', '') for v in i]
            try:
                for v in [1, 2, 3, 4, 5, 6, 8]:
                    i[v] = float(i[v])
            except:
                pass
            tolist.append(i)
        self.__info = (tolist[0][0].split(' ')[1],
                       tolist[0][0].split(' ')[2].decode('big5'))
        self.__RawRowsName = tolist[1]
        return tolist[2:]

    def __serial_fetch(self, no, month):
        """ [list] 串接每月資料 舊→新 """
        re = []
        for i in range(month):
            nowdatetime = datetime.today() - timedelta(30 * i)
            tolist = self.__to_list(self.__fetch_data(no, nowdatetime))
            re = tolist + re
        return re

    def out_putfile(self, fpath):
        """ 輸出成 CSV 檔 """
        op = csv.writer(open(fpath, 'wt'))
        op.writerows(self.__raw_data)

    def __serial_price(self, rows=6):
        """ [list] 取出某一價格序列 舊→新
            預設序列收盤價 → __serial_price(6)
        """
        re = [float(i[rows]) for i in self.__raw_data]
        return re

    def __cal_MA(self, date, row):
        """ 計算移動平均數
            row: 收盤價(6)、成交股數(1)
            回傳 tuple:
                1.序列 舊→新
                2.持續天數
        """
        cal_data = self.__serial_price(row)
        re = []
        for i in range(len(cal_data) - int(date) + 1):
            re.append(round(sum(cal_data[-date:]) / date, 2))
            cal_data.pop()
        re.reverse()
        cont = self.__cal_continue(re)
        return re, cont

    def __cal_continue(self, list_data):
        """ 計算持續天數
            向量數值：正數向上、負數向下。
        """
        diff_data = []
        for i in range(1, len(list_data)):
            if list_data[-i] > list_data[-i - 1]:
                diff_data.append(1)
            else:
                diff_data.append(-1)
        cont = 0
        for v in diff_data:
            if v == diff_data[0]:
                cont += 1
            else:
                break
        return cont * diff_data[0]

    def MA(self, date):
        """ 計算收盤均價與持續天數 """
        return self.__cal_MA(date, 6)

    def MAV(self, date):
        """ 計算成交股數均量與持續天數 """
        val, conti = self.__cal_MA(date, 1)
        val = [round(i / 1000, 3) for i in val]
        return val, conti

    def MAO(self, date1, date2):
        """ 計算乖離率（均價）
            date1 - date2
            回傳 tuple:
                1.序列 舊→新
                2.持續天數
        """
        a = self.MA(date1)[0]
        b = self.MA(date2)[0]
        cal_list = [a[-i] - b[-i] for i in range(1, min(len(a), len(b)) + 1)]
        cal_list.reverse()
        cont = self.__cal_continue(cal_list)
        return cal_list, cont

    @property
    def price(self):
        """ 收盤價股價序列 """
        return self.__serial_price()

    @property
    def openprice(self):
        """ 開盤價股價序列 """
        return self.__serial_price(3)

    @property
    def value(self):
        """ 成交量序列 """
        val = [round(i / 1000, 3) for i in self.__serial_price(1)]
        return val

    def __cal_MAOPoint(self, data, s=5, pm=False):
        """判斷轉折點位置
           s = 取樣判斷區間
           pm = True（正）/False（負）轉折
           return (T/F, 第幾個轉折日, 轉折點值)
        """
        c = data[-s:]
        if pm:  # 正
            ckvalue = max(c)  # 尋找最大值
            preckvalue = max(c) > 0  # 區間最大值必須為正
        else:
            ckvalue = min(c)  # 尋找最小值
            preckvalue = max(c) < 0  # 區間最大值必須為負
        return (s - c.index(ckvalue) < 4 and c.index(ckvalue) != s - 1 \
                and preckvalue,
                s - c.index(ckvalue) - 1,
                ckvalue)

    def ckMAO(self, data, s=5, pm=False):
        """判斷正負乖離轉折點位置
           s = 取樣判斷區間
           pm = True（正）/False（負）乖離
           return (T/F, 第幾轉折日, 乖離轉折點值)
        """
        return self.__cal_MAOPoint(data, s, pm)
