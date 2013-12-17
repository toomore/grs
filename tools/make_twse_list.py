# -*- coding: utf-8 -*-
import csv
import re
import urllib2

TWSEURL = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX2_print.php?genpage=genpage/Report201312/A11220131216%s.php&type=csv'
TWSECLS = {'0049': u'封閉式基金',
           '0099P': u'ETF',
           '019919T': u'受益證券',
           '0999': u'認購權證',  #(不含牛證)
           '0999P': u'認售權證',  #(不含熊證)
           '0999C': u'牛證',
           '0999B': u'熊證',
           '0999GA': u'附認股權特別股',
           '0999GD': u'附認股權公司債',
           '0999G9': u'認股權憑證',
           '01': u'水泥工業',
           '02': u'食品工業',
           '03': u'塑膠工業',
           '04': u'紡織纖維',
           '05': u'電機機械',
           '06': u'電器電纜',
           '07': u'化學生技醫療',
           '21': u'化學工業',
           '22': u'生技醫療業',
           '08': u'玻璃陶瓷',
           '09': u'造紙工業',
           '10': u'鋼鐵工業',
           '11': u'橡膠工業',
           '12': u'汽車工業',
           '13': u'電子工業',
           '24': u'半導體業',
           '25': u'電腦及週邊設備業',
           '26': u'光電業',
           '27': u'通信網路業',
           '28': u'電子零組件業',
           '29': u'電子通路業',
           '30': u'資訊服務業',
           '31': u'其他電子業',
           '14': u'建材營造',
           '15': u'航運業',
           '16': u'觀光事業',
           '17': u'金融保險',
           '18': u'貿易百貨',
           '9299': u'存託憑證',
           '23': u'油電燃氣業',
           '19': u'綜合',
           '20': u'其他',
           'CB': u'可轉換公司債',}
           #'ALL_1': u'全部'}

def fetch_twse_list():
    with open('./twse_list.csv', 'a') as files:
        csv_file = csv.writer(files)
        re_pattern = re.compile(r'(=")?[\d\w]{4,6}(=)?')
        re_sub = re.compile(r'[^\w\d]')

        for no in TWSECLS:
            for i in csv.reader(urllib2.urlopen(TWSEURL % no).readlines()):
                if len(i) >= 3 and re_pattern.match(i[0]):
                    pass
                else:
                    i.pop(0)

                if len(i) >= 2 and re_pattern.match(i[0]):
                    csv_file.writerow([re_sub.sub('', i[0]),
                                       i[1].decode('cp950').encode('utf-8'),
                                       TWSECLS[no].encode('utf-8')])

    with open('./twse_list.csv', 'r') as files:
        csv_file = csv.reader(files)
        all_items = {}
        for i in csv_file:
            all_items.update({i[0]: i})

    with open('./twse_list.csv', 'w') as files:
        csv_file = csv.writer(files)
        for i in sorted(all_items):
            csv_file.writerow(all_items[i])

def output_industry_code():
    with open('./industry_code.csv', 'w') as files:
        csv_file = csv.writer(files)
        for i in sorted(TWSECLS):
            csv_file.writerow([i, TWSECLS[i].encode('utf-8')])

if __name__ == '__main__':
    fetch_twse_list()
    output_industry_code()
