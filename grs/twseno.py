# -*- coding: utf-8 -*-
''' TWSE stock no. '''
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
import csv
import os
import re


class TWSENo(object):
    """ 上市股票代碼與搜尋 """
    def __init__(self):
        self.last_update = ''
        self.__allstockno = self.__importcsv()

    def __importcsv(self):
        ''' import data from csv '''
        csv_path = os.path.join(os.path.dirname(__file__), 'stock_no.csv')
        with open(csv_path) as csv_file:
            csv_data = csv.reader(csv_file)
            result = {}
            for i in csv_data:
                try:
                    result[int(i[0])] = str(i[1]).decode('utf-8')
                except ValueError:
                    if i[0] == 'UPDATE':
                        self.last_update = str(i[1]).decode('utf-8')
                    else:
                        pass
        return result

    @staticmethod
    def __industry_code():
        ''' import industry_code '''
        csv_path = os.path.join(os.path.dirname(__file__), 'industry_code.csv')
        with open(csv_path) as csv_file:
            csv_data = csv.reader(csv_file)
            result = {}
            for i in csv_data:
                result[i[0]] = i[1].decode('utf-8')
            return result

    @staticmethod
    def __loadindcomps():
        ''' import industry comps '''
        csv_path = os.path.join(os.path.dirname(__file__), 'stock_no.csv')
        with open(csv_path) as csv_file:
            csv_data = csv.reader(csv_file)
            result = {}
            check_words = re.compile(r'^[\d]{2,}[\w]?')
            for i in csv_data:
                if check_words.match(i[2]):
                    try:
                        result[i[2]].append(i[0].decode('utf-8'))
                    except (ValueError, KeyError):
                        try:
                            result[i[2]] = [i[0].decode('utf-8')]
                        except KeyError:
                            pass
            return result

    def search(self, name):
        """ 搜尋股票名稱 by unicode

            :param str name: 欲搜尋的字串
            :rtype: list
        """
        pattern = re.compile(name)
        result = {}
        for i in self.__allstockno:
            query = re.search(pattern, self.__allstockno[i])
            if query:
                query.group()
                result[i] = self.__allstockno[i]
        return result

    def searchbyno(self, name):
        """ 搜尋股票代碼

            :param str name: 欲搜尋的字串
            :rtype: list
        """
        pattern = re.compile(str(name))
        result = {}
        for i in self.__allstockno:
            query = re.search(pattern, str(i))
            if query:
                query.group()
                result[i] = self.__allstockno[i]
        return result

    @property
    def all_stock(self):
        """ 回傳上市股票代碼與名稱

            :rtype: dict
        """
        return self.__allstockno

    @property
    def all_stock_no(self):
        """ 回傳上市股票代碼

            :rtype: list
        """
        return self.__allstockno.keys()

    @property
    def all_stock_name(self):
        """ 回傳上市股票名稱

            :rtype: list
        """
        return self.__allstockno.values()

    @property
    def industry_code(self):
        """ 回傳類別代碼

            :rtype: dict
        """
        return self.__industry_code()

    @property
    def industry_comps(self):
        """ 回傳分類的股票

            :rtype: dict
        """
        return self.__loadindcomps()
