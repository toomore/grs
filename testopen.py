#!/usr/bin/env python
# -*- coding: utf-8 -*-
from grs import twseopen
from datetime import datetime

t = twseopen()

print t.Dday(datetime.today())
print t.Dday(datetime(2012, 12, 22))
