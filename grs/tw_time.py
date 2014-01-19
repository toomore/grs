# -*- coding: utf-8 -*-
''' Taiwan time UTF+8  '''
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
from datetime import time
from datetime import timedelta


class TWTime(object):
    ''' Transform localtime to Taiwan time in UTF+8
        轉換當地時間到台灣時間 UTF+8

        :param int tz: 時區，預設為 8
    '''

    def __init__(self, tz=8):
        assert isinstance(tz, (int, float))
        self.time_zone = tz

    def now(self):
        ''' Display Taiwan Time now
            顯示台灣此刻時間
        '''
        utcnow = datetime.utcnow()
        return utcnow + timedelta(hours=self.time_zone)

    def date(self):
        ''' Display Taiwan date now
            顯示台灣此刻日期
        '''
        utcnow = datetime.utcnow()
        return (utcnow + timedelta(hours=self.time_zone)).date()

    @staticmethod
    def localtime():
        ''' Display localtime now
            顯示當地此刻時間
        '''
        return datetime.now()

    @staticmethod
    def localdate():
        ''' Display localdate now
            顯示當地此刻日期
        '''
        return datetime.today().date()


class Countdown(object):
    ''' 倒數

        :param int hour: 設定倒數的時刻小時，預設為 14
        :param int minutes: 設定倒數的時刻分鐘，預設為 30
    '''
    def __init__(self, hour=14, minutes=30):
        self.__back = timedelta(hours=hour - 8, minutes=minutes)
        self.__hour = hour
        self.__minutes = minutes

    @property
    def __zero(self):
        ''' 取得現在時間（秒） '''
        return datetime.utcnow() - self.__back

    @property
    def nextday(self):
        ''' nextday: 下一個日期

            :rtype: datetime
            :returns: 下一個預設時間日期
        '''
        nextday = self.__zero.date() + timedelta(days=1)
        return datetime.combine(nextday, time())

    @property
    def countdown(self):
        ''' countdown: 到達下一個日期的秒數

            :rtype: int
            :returns: 下一個預設的秒數
        '''
        return (self.nextday - self.__zero).seconds

    @property
    def exptime(self):
        ''' exptime: 下一個日期時間

            :returns: 下一個預設時間
        '''
        return self.nextday + timedelta(hours=self.__hour - 8,
                                        minutes=self.__minutes)

    @property
    def lastmod(self):
        ''' lastmod: 起點日期時間

            :returns: 起點日期時間
        '''
        return self.exptime - timedelta(days=1)
