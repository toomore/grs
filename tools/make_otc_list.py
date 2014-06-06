# -*- coding: utf-8 -*-
import csv
import re
import urllib2
from datetime import datetime


NOW = datetime(2014, 2, 21)
SAVEPATH = '../grs/otc_list.csv'
INDUSTRYCODE = '../grs/industry_code_otc.csv'

OTCURL = 'http://www.gretai.org.tw/ch/stock/aftertrading/otc_quotes_no1430/stk_wn1430_download.php?d=%(year)s/%(mon)02d/%(day)02d&se=%%s&s=0,asc,0' % {
        'year': NOW.year - 1911,
        'mon': NOW.month,
        'day': NOW.day,}

OTCCLS = {
           '01': u'水泥工業',
           '02': u'食品工業',
           '03': u'塑膠工業',
           '04': u'紡織纖維',
           '05': u'電機機械',
           '06': u'電器電纜',
           '07': u'化學生技醫療',
           '08': u'玻璃陶瓷',
           '09': u'造紙工業',
           '10': u'鋼鐵工業',
           '11': u'橡膠工業',
           '12': u'汽車工業',
           '13': u'電子工業',
           '14': u'建材營造',
           '15': u'航運業',
           '16': u'觀光事業',
           '17': u'金融保險',
           '18': u'貿易百貨',
           '19': u'綜合',
           '20': u'其他',
           '21': u'化學工業',
           '22': u'生技醫療業',
           '23': u'油電燃氣業',
           '24': u'半導體業',
           '25': u'電腦及週邊設備業',
           '26': u'光電業',
           '27': u'通信網路業',
           '28': u'電子零組件業',
           '29': u'電子通路業',
           '30': u'資訊服務業',
           '31': u'其他電子業',
           '32': u'文化創意業',
           '80': u'管理股票',
           'AA': u'受益證券',
           'EE': u'上櫃指數股票型基金(ETF)',
           'TD': u'台灣存託憑證(TDR)',
           'WW': u'認購售權證',
           'GG': u'認股權憑證',
           'BC': u'牛證熊證',
           #'EW': u'所有證券(不含權證、牛熊證)',
           #'AL': u'所有證券 ',
           #'OR': u'委託及成交資訊(16:05提供)',
           }

def fetch_otc_list():
    with open(SAVEPATH, 'w') as files:
        csv_file = csv.writer(files)
        re_pattern = re.compile(r'(=")?[\d\w]{4,6}(=)?')
        re_sub = re.compile(r'[^\w\d]')

        for no in OTCCLS:
            for i in csv.reader(urllib2.urlopen(OTCURL % no).readlines()):
                if len(i) >= 3 and re_pattern.match(i[0]):
                    pass
                else:
                    i.pop(0)

                if len(i) >= 2 and re_pattern.match(i[0]):
                    csv_file.writerow([re_sub.sub('', i[0]),
                                       i[1].decode('cp950').encode('utf-8'),
                                       no, OTCCLS[no].encode('utf-8')])

    with open(SAVEPATH, 'r') as files:
        csv_file = csv.reader(files)
        all_items = {}
        for i in csv_file:
            all_items.update({i[0]: i})

    with open(SAVEPATH, 'w') as files:
        csv_file = csv.writer(files)
        #csv_file.writerow(['文件更新', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'x', 'x'])
        csv_file.writerow(['UPDATE', datetime.now().strftime('%Y/%m/%d'), 'x', 'x'])
        csv_file.writerow(['證期會代碼', '公司簡稱', '分類代碼', '分類名稱'])
        for i in sorted(all_items):
            csv_file.writerow(all_items[i])

def output_industry_code():
    with open(INDUSTRYCODE, 'w') as files:
        csv_file = csv.writer(files)
        for i in sorted(OTCCLS):
            csv_file.writerow([i, OTCCLS[i].encode('utf-8')])

if __name__ == '__main__':
    fetch_otc_list()
    output_industry_code()
