# -*- coding: utf-8 -*-
import time
import ujson as json
import urllib3
from datetime import datetime

URL = urllib3.connection_from_url('http://mis.tse.com.tw/',
        headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0',
                 #'Accept-Language': 'en-US'})
                 'Accept-Language': 'zh-TW'})

#STOCKPATH = '/stock/api/getStockInfo.jsp?ex_ch=tse_1101.tw_20140530&json=1&delay=0&_=1401450118102'
STOCKPATH = '/stock/api/getStockInfo.jsp?ex_ch=%(etype)s_%(no)s.tw_%(date)s&json=1&delay=0&_=%(timestamp)s'

class Realtime(object):
    def __init__(self, no, date):
        if not date:
            date = datetime.now()

        params = {'no': no, 'etype': self._etype,
                  'date': date.strftime('%Y%m%d'),
                  'timestamp': int(time.time())}

        self.result = URL.request('GET', STOCKPATH % params)
        self.data = json.loads(self.result.data)

class RealtimeStock(Realtime):
    _etype = 'tse'

    def __init__(self, no, date=None):
        super(RealtimeStock, self).__init__(no, date)

if __name__ == '__main__':
    print RealtimeStock(2618).data
