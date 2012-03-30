#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grs import stock


a = stock(2618)
'''
print 'Row Data'
print a.row_data
print '=' * 20
print 'Row 6 Data'
print a.serial_price(6)
print '=' * 20
'''
print 'MA3'
print '=' * 20
print a.MA(3)
print a.MAV(3)
print ''
print 'MA6'
print '=' * 20
print a.MA(6)
print a.MAV(6)
print ''
print 'MA18'
print '=' * 20
print a.MA(18)
print a.MAV(18)
print ''
print 'VAL'
print '=' * 20
print a.MAV(1)
