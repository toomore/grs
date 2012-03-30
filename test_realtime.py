#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grs import rt_stock
from grs import rt_weight


r = rt_stock(2618)
print 'real'
print '=' * 20
#for i in r.real:
    #print i, r.real[i]
print r.real
print 'raw'
print '=' * 20
print r.raw
rw = rt_weight()
print 'weight'
print '=' * 20
print rw.real
