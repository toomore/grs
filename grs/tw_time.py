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
from datetime import timedelta


class TWTime(object):
    ''' Transform localtime to Taiwan time in UTF+8
        轉換當地時間到台灣時間 UTF+8
    '''
    def __init__(self, tz=8):
        try:
            self.TimeZone = float(tz)
        except:
            self.TimeZone = 8

    @property
    def now(self):
        ''' Display Taiwan Time now
            顯示台灣此刻時間
        '''
        utcnow = datetime.utcnow()
        return utcnow + timedelta(hours=self.TimeZone)

    @property
    def date(self):
        ''' Display Taiwan date now
            顯示台灣此刻日期
        '''
        utcnow = datetime.utcnow()
        return (utcnow + timedelta(hours=self.TimeZone)).date()

    @property
    def localtime(self):
        ''' Display localtime now
            顯示當地此刻時間
        '''
        return datetime.now()

    @property
    def localdate(self):
        ''' Display localdate now
            顯示當地此刻日期
        '''
        return datetime.today().date()


class Countdown(object):
    """ 倒數
        nextday: 下一個日期
        countdown: 到達下一個日期的秒數
        exptime: 下一個日期時間
        lastmod: 起點日期時間
    """
    def __init__(self, h=14, m=30):
        self.__back = timedelta(hours=h - 8, minutes=m)
        self.__zero = datetime.utcnow() - self.__back
        self.nextday = datetime(self.__zero.year,
                                self.__zero.month,
                                self.__zero.day + 1)
        self.countdown = (self.nextday - self.__zero).seconds
        self.exptime = self.nextday + timedelta(hours=h - 8, minutes=m)
        self.lastmod = self.exptime - timedelta(days=1)
