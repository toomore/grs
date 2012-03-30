#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grs import B4P, stock, twseno

l = twseno().AllStockNo

for i in l:
    try:
        BS, info = B4P(stock(i)).B4Point()
        if BS:  # 買點
            print 'B: {0} {1}'.format(i, info)
        else:   # 賣點
            print 'S: {0} {1}'.format(i, info)
    except:     # 不作為或資料不足
        print 'X: {0}'.format(i)
