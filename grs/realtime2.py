# -*- coding: utf-8 -*-
import time
import ujson as json
import urllib3
from datetime import datetime

URL = urllib3.connection_from_url('http://mis.tse.com.tw/',
        #headers={'Accept-Language': 'en-US'})
        headers={'Accept-Language': 'zh-TW'})

#STOCKPATH = '/stock/api/getStockInfo.jsp?ex_ch=tse_1101.tw_20140530&json=1&delay=0&_=1401450118102'
STOCKPATH = '/stock/api/getStockInfo.jsp?ex_ch=%(exchange)s_%(no)s.tw_%(date)s&json=1&delay=%(delay)s&_=%(timestamp)s'
#WEIGHTPATH = '/stock/api/getStockInfo.jsp?ex_ch=tse_t00.tw|otc_o00.tw|tse_FRMSA.tw&json=1&delay=0&_=1401464211663'
WEIGHTPATH = '/stock/api/getStockInfo.jsp?ex_ch=tse_t00.tw_%(date)s|otc_o00.tw_%(date)s|tse_FRMSA.tw_%(date)s&json=1&delay=%(delay)s&_=%(timestamp)s'


class Realtime(object):
    def __init__(self, no, date, delay=0):
        if not date:
            date = datetime.now()

        params = {'no': no, 'exchange': self._exchange,
                  'date': date.strftime('%Y%m%d'),
                  'timestamp': int(time.time()),
                  'delay': delay}

        self.result = URL.request('GET', STOCKPATH % params)
        self.raw = json.loads(self.result.data)
        self.data = self.make_format(self.raw)

    @staticmethod
    def make_format(raw):
        data = {}
        for i in raw['msgArray']:
            if i['c'] not in data:
                data[i['c']] = {}

            best_ask_price = [float(v) for v in i['a'].split('_')[:-1]]
            best_bid_price = [float(v) for v in i['b'].split('_')[:-1]]
            best_ask_volume = [int(v) for v in i['f'].split('_')[:-1]]
            best_bid_volume = [int(v) for v in i['g'].split('_')[:-1]]

            data[i['c']]['best_ask_list'] = zip(best_ask_price, best_ask_volume)
            data[i['c']]['best_bid_list'] = zip(best_bid_price, best_bid_volume)
            data[i['c']]['best_ask_price'] = best_ask_price[0]
            data[i['c']]['best_ask_volume'] = best_ask_volume[0]
            data[i['c']]['best_bid_price'] = best_bid_price[0]
            data[i['c']]['best_bid_volume'] = best_bid_volume[0]
            data[i['c']]['open'] = float(i['o'])
            data[i['c']]['highest'] = float(i['h'])
            data[i['c']]['lowest'] = float(i['l'])
            data[i['c']]['price'] = float(i['z'])
            data[i['c']]['limit_up'] = float(i['u'])
            data[i['c']]['limit_down'] = float(i['w'])
            data[i['c']]['volume'] = float(i['tv'])
            data[i['c']]['volume_acc'] = float(i['v'])
            data[i['c']]['yesterday_price'] = float(i['y'])

            diff = data[i['c']]['price'] - data[i['c']]['open']
            diff_percent = round(diff / data[i['c']]['open'] * 100, 2)
            data[i['c']]['diff'] = (round(diff, 2), diff_percent)

            data[i['c']]['info'] = {'name': i['n'],
                                    'full_name': i['nf'],
                                    'no': i['c'],
                                    'ticker': i['ch'],
                                    'exchange': i['ex'],
                                   }

        return data


class RealtimeTESE(Realtime):
    _exchange = 'tse'

    def __init__(self, no, date=None):
        super(RealtimeTESE, self).__init__(no, date)


class RealtimeOTC(Realtime):
    _exchange = 'otc'

    def __init__(self, no, date=None):
        super(RealtimeOTC, self).__init__(no, date)


class RealtimeWeight(object):
    def __init__(self, date=None, delay=0):
        if not date:
            date = datetime.now()

        params = {'date': date.strftime('%Y%m%d'),
                  'timestamp': int(time.time()),
                  'delay': delay}

        self.result = URL.request('GET', WEIGHTPATH % params)
        self.raw = json.loads(self.result.data)
        self.data = self.make_format(self.raw)

    @staticmethod
    def make_format(raw):
        data = {}
        for i in raw['msgArray']:
            if i['c'] not in data:
                data[i['c']] = {}

            data[i['c']]['open'] = float(i['o'])
            data[i['c']]['highest'] = float(i['h'])
            data[i['c']]['lowest'] = float(i['l'])
            data[i['c']]['price'] = float(i['z'])
            data[i['c']]['volume'] = float(i['tv']) if i['tv'] != '-' else 0
            data[i['c']]['volume_acc'] = float(i['v']) if 'v' in i else 0
            data[i['c']]['yesterday_price'] = float(i['y'])

            diff = data[i['c']]['price'] - data[i['c']]['open']
            diff_percent = round(diff / data[i['c']]['open'] * 100, 2)
            data[i['c']]['diff'] = (round(diff, 2), diff_percent)

            data[i['c']]['info'] = {'name': i['n'],
                                    'no': i['c'],
                                    'ticker': i['ch'],
                                    'exchange': i['ex'],
                                   }

        return data

if __name__ == '__main__':
    from pprint import pprint
    realtime_data = RealtimeTESE(1201, datetime(2014, 6, 6))
    pprint(realtime_data.raw)
    pprint(realtime_data.data)
    #pprint(RealtimeOTC(8446, datetime(2014, 6, 5)).data)
    realtime_weight = RealtimeWeight(datetime(2014, 6, 6))
    pprint(realtime_weight.raw)
    pprint(realtime_weight.data)
