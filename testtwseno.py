#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grs import twseno


t = twseno()
print dir(t)

t.AllStock  # 所有股票代碼 type: dict

''' IndCode
for i in t.IndComps:  # 回傳類別所屬股票代碼 type: dict
    print i,t.IndComps[i]
'''
print t.LastUpdate
'''
'last_update', 'search', 'searchbyno'
'''
print t.search('中') # 搜尋股票名稱，回傳 type: dict
print t.searchbyno(23) # 搜尋股票名稱，回傳 type: dict
