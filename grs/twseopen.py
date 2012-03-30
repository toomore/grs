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

from datetime import datetime
from .tw_time import TWTime
import csv
import os


class twseopen(object):
    ''' 判斷當日是否開市 '''
    def __init__(self):
        ''' 載入相關檔案 '''
        self.__ocdate = self.__loaddate()

    def Dday(self, time):
        ''' 指定日期 '''
        if type(time) == type(TWTime().now):
            self.twtime = TWTime().now
        elif type(time) == type(TWTime().date):
            self.twtime = TWTime().date
        else:
            pass
        return self.__caldata(time)

    def __loaddate(self):
        ''' 載入檔案
            檔案依據 http://www.twse.com.tw/ch/trading/trading_days.php
        '''
        ld = csv.reader(
                open(os.path.join(os.path.dirname(__file__), 'opendate.csv')))
        re = {}
        re['close'] = []
        re['open'] = []
        for i in ld:
            if i[1] == '0':  # 0 = 休市
                re['close'] += [datetime.strptime(i[0], '%Y/%m/%d').date()]
            elif i[1] == '1':  # 1 = 開市
                re['open'] += [datetime.strptime(i[0], '%Y/%m/%d').date()]
            else:
                pass
        return re

    def __caldata(self, time):
        ''' Market open or not.
            回傳 True：開市，False：休市。
        '''
        if time.date() in self.__ocdate['close']:  # 判對是否為法定休市
            return False
        elif time.date() in self.__ocdate['open']:  # 判對是否為法定開市
            return True
        else:
            if time.weekday() <= 4:  # 判斷是否為平常日開市
                return True
            else:
                return False
