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


class ImportCSV(object):
    """ Import CSV

        :param path stock_no_files: 個股檔案列表
        :param path industry_code_files: 個股分類表
    """
    def __init__(self, stock_no_files, industry_code_files):
        self.industry_code_files = industry_code_files
        self.last_update = ''
        self.stock_no_files = stock_no_files
        self.__allstockno = self.importcsv()

    def importcsv(self):
        ''' import data from csv '''
        csv_path = os.path.join(os.path.dirname(__file__), self.stock_no_files)
        with open(csv_path) as csv_file:
            csv_data = csv.reader(csv_file)
            result = {}
            for i in csv_data:
                try:
                    result[i[0]] = str(i[1]).decode('utf-8')
                except ValueError:
                    if i[0] == 'UPDATE':
                        self.last_update = str(i[1]).decode('utf-8')
                    else:
                        pass
        return result

    def __industry_code(self):
        ''' import industry_code '''
        csv_path = os.path.join(os.path.dirname(__file__),
                self.industry_code_files)
        with open(csv_path) as csv_file:
            csv_data = csv.reader(csv_file)
            result = {}
            for i in csv_data:
                result[i[0]] = i[1].decode('utf-8')
            return result

    def __loadindcomps(self):
        ''' import industry comps '''
        csv_path = os.path.join(os.path.dirname(__file__), self.stock_no_files)
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
            :rtype: dict
        """
        pattern = re.compile(name)
        result = {}
        for i in self.__allstockno:
            query = re.search(pattern, self.__allstockno[i])
            if query:
                query.group()
                result[i] = self.__allstockno[i]
        return result

    def searchbyno(self, no):
        """ 搜尋股票代碼

            :param str no: 欲搜尋的字串
            :rtype: dict
        """
        pattern = re.compile(str(no))
        result = {}
        for i in self.__allstockno:
            query = re.search(pattern, str(i))
            if query:
                query.group()
                result[i] = self.__allstockno[i]
        return result

    @property
    def all_stock(self):
        """ 回傳股票代碼與名稱

            :rtype: dict
        """
        return self.__allstockno

    @property
    def all_stock_no(self):
        """ 回傳股票代碼

            :rtype: list
        """
        return self.__allstockno.keys()

    @property
    def all_stock_name(self):
        """ 回傳股票名稱

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

    def get_stock_comps_list(self):
        """ 回傳日常交易的類別代碼與名稱

            :rtype: dict

            .. versionadded:: 0.5.6
        """
        code_list = self.industry_code
        stock_comps_list = {}

        for i in code_list:
            if len(i) == 2 and i.isdigit():
                stock_comps_list.update({i: code_list[i]})

        return stock_comps_list

    def get_stock_list(self):
        """ 回傳日常交易的代碼與名稱

            :rtype: dict

            .. versionadded:: 0.5.6
        """
        all_stock = self.all_stock
        industry_comps = self.industry_comps
        result = {}

        for comps_no in self.get_stock_comps_list():
            if comps_no in industry_comps:
                for stock_no in industry_comps[comps_no]:
                    result.update({stock_no: all_stock[stock_no]})
        return result

class TWSENo(ImportCSV):
    """ 上市股票代碼與搜尋 """
    def __init__(self):
        super(TWSENo, self).__init__('twse_list.csv', 'industry_code.csv')


class OTCNo(ImportCSV):
    """ 上櫃股票(OTC, Over-the-counter) 代碼與搜尋"""
    def __init__(self):
        super(OTCNo, self).__init__('otc_list.csv', 'industry_code_otc.csv')


if __name__ == '__main__':
    t = TWSENo()
    #t = OTCNo()
    t_list = t.get_stock_list()
    print t_list
