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


class B4P(object):
    """ 四大買點組合 """
    def __init__(self, a):
        self.a = a

    def GLI(self, pm=False):
        """ 判斷乖離 """
        return self.a.ckMAO(self.a.MAO(3, 6)[0], pm=pm)[0]

    def ckPlusGLI(self):
        """ 正乖離扣至最大 """
        return self.GLI(True)

    def ckMinsGLI(self):
        """ 負乖離扣至最大 """
        return self.GLI()

    ##### 四大買點 #####
    def B1(self):
        """ 量大收紅 """
        re = self.a.value[-1] > self.a.value[-2] and \
             self.a.price[-1] > self.a.openprice[-1]
        return re

    def B2(self):
        """ 量縮價不跌 """
        re = self.a.value[-1] < self.a.value[-2] and \
             self.a.price[-1] > self.a.price[-2]
        return re

    def B3(self):
        """ 三日均價由下往上 """
        return self.a.MA(3)[1] == 1

    def B4(self):
        """ 三日均價大於六日均價 """
        return self.a.MA(3)[0][-1] > self.a.MA(6)[0][-1]

    ##### 四大賣點 #####
    def S1(self):
        """ 量大收黑 """
        re = self.a.value[-1] > self.a.value[-2] and \
             self.a.price[-1] < self.a.openprice[-1]
        return re

    def S2(self):
        """ 量縮價跌 """
        re = self.a.value[-1] < self.a.value[-2] and \
             self.a.price[-1] < self.a.price[-2]
        return re

    def S3(self):
        """ 三日均價由上往下 """
        return self.a.MA(3)[1] == -1

    def S4(self):
        """ 三日均價小於六日均價 """
        return self.a.MA(3)[0][-1] < self.a.MA(6)[0][-1]

    def B4PB(self):
        """ 判斷是否為四大買點 """
        re = []
        if self.ckMinsGLI() and \
            (self.B1() or self.B2() or self.B3() or self.B4()):
            if self.B1():
                re.append(self.B1.__doc__.strip())
            if self.B2():
                re.append(self.B2.__doc__.strip())
            if self.B3():
                re.append(self.B3.__doc__.strip())
            if self.B4():
                re.append(self.B4.__doc__.strip())
            re = ', '.join(re)
        else:
            re = False
        return re

    def B4PS(self):
        """ 判斷是否為四大賣點 """
        re = []
        if self.ckPlusGLI() and \
            (self.S1() or self.S2() or self.S3() or self.S4()):
            if self.S1():
                re.append(self.S1.__doc__.strip())
            if self.S2():
                re.append(self.S2.__doc__.strip())
            if self.S3():
                re.append(self.S3.__doc__.strip())
            if self.S4():
                re.append(self.S4.__doc__.strip())
            re = ', '.join(re)
        else:
            re = False
        return re

    def B4Point(self):
        """ 判斷買點或賣點 """
        b = self.B4PB()
        s = self.B4PS()
        if b:
            return True,b
        if s:
            return False,s
