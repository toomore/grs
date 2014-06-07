# -*- coding: utf-8 -*-
import time
import ujson as json
import urllib3
from datetime import datetime

URL = urllib3.connection_from_url('http://mis.tse.com.tw/',
        #headers={'Accept-Language': 'en-US'})
        headers={'Accept-Language': 'zh-TW'})

#STOCKPATH = '/stock/api/getStockInfo.jsp?ex_ch=tse_1101.tw_20140530&json=1&delay=0&_=1401450118102'
STOCKPATH = '/stock/api/getStockInfo.jsp?ex_ch=%(etype)s_%(no)s.tw_%(date)s&json=1&delay=%(delay)s&_=%(timestamp)s'


class Realtime(object):
    def __init__(self, no, date, delay=0):
        if not date:
            date = datetime.now()

        params = {'no': no, 'etype': self._etype,
                  'date': date.strftime('%Y%m%d'),
                  'timestamp': int(time.time()),
                  'delay': delay}

        self.result = URL.request('GET', STOCKPATH % params)
        self.data = json.loads(self.result.data)


class RealtimeTESE(Realtime):
    _etype = 'tse'

    def __init__(self, no, date=None):
        super(RealtimeTESE, self).__init__(no, date)


class RealtimeOTC(Realtime):
    _etype = 'otc'

    def __init__(self, no, date=None):
        super(RealtimeOTC, self).__init__(no, date)


if __name__ == '__main__':
    from pprint import pprint
    pprint(RealtimeTESE(2618, datetime(2014, 6, 5)).data)
    pprint(RealtimeOTC(8446, datetime(2014, 6, 5)).data)
