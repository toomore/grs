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
import csv
import os


class twseno(object):
    """ 上市股票代碼與搜尋 """
    def __init__(self):
        self.__allstockno = self.__importcsv()

    def __importcsv(self):
        f = csv.reader(
            open(os.path.join(os.path.dirname(__file__), 'stock_no.csv')))
        re = {}
        for i in f:
            try:
                re[int(i[0])] = str(i[1])
            except:
                if i[0] == 'UPDATE':
                    self.LastUpdate = str(i[1])
                else:
                    pass
        return re

    def __industry_code(self):
        f = csv.reader(
            open(os.path.join(os.path.dirname(__file__), 'industry_code.csv')))
        re = {}
        for i in f:
            re[int(i[0])] = i[1]
        return re

    def __loadindcomps(self):
        f = csv.reader(
            open(os.path.join(os.path.dirname(__file__), 'stock_no.csv')))
        re = {}
        for i in f:
            try:
                re[int(i[2])].append(i[0])
            except:
                try:
                    re[int(i[2])] = [i[0]]
                except:
                    pass
        return re

    def search(self, q):
        """ 搜尋股票名稱 """
        import re
        pattern = re.compile(q)
        result = {}
        for i in self.__allstockno:
            b = re.search(pattern, self.__allstockno[i])
            try:
                b.group()
                result[i] = self.__allstockno[i]
            except:
                pass
        return result

    def searchbyno(self, q):
        """ 搜尋股票代碼 """
        import re
        pattern = re.compile(str(q))
        result = {}
        for i in self.__allstockno:
            b = re.search(pattern, str(i))
            try:
                b.group()
                result[i] = self.__allstockno[i]
            except:
                pass
        return result

    @property
    def AllStock(self):
        """ 回船上市股票代碼與名稱 type: dict """
        return self.__allstockno

    @property
    def AllStockNo(self):
        """ 回船上市股票代碼 type: list """
        return self.__allstockno.keys()

    @property
    def AllStockName(self):
        """ 回船上市股票名稱 type: list """
        return self.__allstockno.values()

    @property
    def IndCode(self):
        """ 回傳類別代碼 by dict """
        return self.__industry_code()

    @property
    def IndComps(self):
        """ 回傳分類的股票 by dict """
        return self.__loadindcomps()
