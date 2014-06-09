# -*- coding: utf-8 -*-
''' Get TWSE real time data. '''
# From http://github.com/toomore/tw-stock
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
import logging
import random
import urllib3
from .error import ConnectionError

TSE_URL = 'http://mis.tse.com.tw/'
TSE_CONNECTIONS = urllib3.connection_from_url(TSE_URL)

def covstr(strings):
    """ convert string to int or float. """
    try:
        result = int(strings)
    except ValueError:
        result = float(strings)
    return result


class RealtimeStock(object):
    """ Real time fetch TW stock data.
        擷取即時盤的股價資訊

        :param str no: 股票代碼
        :rtype: dict
    """
    def __init__(self, no):
        assert isinstance(no, basestring), '`no` must be a string'
        self.__raw = ''
        try:
            page = TSE_CONNECTIONS.urlopen('GET', '/data/%s.csv?r=%s' % (no,
                        random.randrange(1, 10000))).data
        except urllib3.exceptions.HTTPError:
            raise ConnectionError(), u'IN OFFLINE, NO DATA FETCH.'

        logging.info('twsk no %s', no)
        reader = csv.reader(page.split('\r\n'))
        for i in reader:
            if i:
                self.__raw = i

    @property
    def raw(self):
        ''' Return raw data

            :rtype: list
            :returns: raw data list
        '''
        return self.__raw

    @property
    def real(self):
        """ Real time data

            :rtype: dict
            :returns:

                :name:     股票名稱 Unicode
                :no:       股票代碼
                :range:    漲跌價
                :ranges:   漲跌判斷 True, False
                :time:     取得時間
                :max:      漲停價
                :min:      跌停價
                :unch:     昨日收盤價
                :pp:       漲跌幅 %
                :o:        開盤價
                :h:        當日最高價
                :l:        當日最低價
                :c:        成交價/收盤價
                :value:    累計成交量
                :pvalue:   該盤成交量
                :top5buy:  最佳五檔買進價量資訊
                :top5sell: 最佳五檔賣出價量資訊
                :crosspic: K線圖 by Google Chart
        """
        try:
            unch = sum([covstr(self.__raw[3]), covstr(self.__raw[4])]) / 2
            result = {
            'name': unicode(self.__raw[36].replace(' ', ''), 'cp950'),
            'no': self.__raw[0],
            'range': self.__raw[1],    # 漲跌價
            'time': self.__raw[2],     # 取得時間
            'max': self.__raw[3],      # 漲停價
            'min': self.__raw[4],      # 跌停價
            'unch': '%.2f' % unch,  # 昨日收盤價
            'pp': '%.2f' % ((covstr(self.__raw[8]) - unch) / unch * 100),
                                       # 漲跌幅 %
            'o': self.__raw[5],        # 開盤價
            'h': self.__raw[6],        # 當日最高價
            'l': self.__raw[7],        # 當日最低價
            'c': self.__raw[8],        # 成交價/收盤價
            'value': self.__raw[9],    # 累計成交量
            'pvalue': self.__raw[10],  # 該盤成交量
            'top5buy': [
                            (self.__raw[11], self.__raw[12]),
                            (self.__raw[13], self.__raw[14]),
                            (self.__raw[15], self.__raw[16]),
                            (self.__raw[17], self.__raw[18]),
                            (self.__raw[19], self.__raw[20])
                            ],
            'top5sell': [
                            (self.__raw[21], self.__raw[22]),
                            (self.__raw[23], self.__raw[24]),
                            (self.__raw[25], self.__raw[26]),
                            (self.__raw[27], self.__raw[28]),
                            (self.__raw[29], self.__raw[30])
                            ]
            }

            if '-' in self.__raw[1]:  # 漲跌判斷 True, False
                result['ranges'] = False  # price down
            else:
                result['ranges'] = True  # price up

            result['crosspic'] = ("http://chart.apis.google.com/chart?" +
                "chf=bg,s,ffffff&chs=20x50&cht=ls" +
                "&chd=t1:0,0,0|0,%(h)s,0|0,%(c)s,0|0,%(o)s,0|0,%(l)s,0" +
                "&chds=%(l)s,%(h)s&chm=F,,1,1:4,20") % result

            result['top5buy'].sort()
            result['top5sell'].sort()

            return result
        except (IndexError, ValueError):
            return False


class RealtimeWeight(object):
    """ 大盤/各類別即時盤資訊

        代碼可以參考：http://goristock.appspot.com/API#apiweight
    """
    def __init__(self):
        """ 大盤/各類別即時盤資訊
            代碼可以參考：http://goristock.appspot.com/API#apiweight
        """
        self.__raw = {}
        try:
            page = TSE_CONNECTIONS.urlopen('GET',
                    '/data/TSEIndex.csv?r=%s' % random.randrange(1, 10000)).data
        except urllib3.exceptions.HTTPError:
            raise ConnectionError(), u'IN OFFLINE, NO DATA FETCH.'

        reader = csv.reader(page.split('\r\n'))
        for i in reader:
            if i:
                if '-' in i[3]:
                    up_or_down = False
                else:
                    up_or_down = True
                self.__raw[i[0]] = {
                                    'no': i[0],
                                    'time': i[1],
                                    'value': i[2],
                                    'range': i[3],
                                    'up_or_down': up_or_down}
        # 大盤成交量，單位：億。
        self.__raw['200']['v2'] = int(
                    self.__raw['200']['value'].replace(',', '')) / 100000000

    @property
    def raw(self):
        ''' Return raw data

            :rtype: list
            :returns: raw data list
        '''
        return self.__raw

    @property
    def real(self):
        ''' Get realtime data

            :rtype: dict
            :returns: 代碼可以參考：http://goristock.appspot.com/API#apiweight
        '''
        result = self.__raw['1'].copy()
        result['c'] = self.__raw['1']['value']
        result['value'] = self.__raw['200']['v2']
        result['date'] = self.__raw['0']['time']
        return result
