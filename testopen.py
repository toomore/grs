#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from grs import TWSEOpen

t = TWSEOpen()

print t.d_day(datetime.today())
print t.d_day(datetime(2014, 1, 1))
