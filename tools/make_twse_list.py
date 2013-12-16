# -*- coding: utf-8 -*-
import csv
import re
import urllib2

TWSEURL = 'http://www.twse.com.tw/ch/trading/exchange/MI_INDEX/MI_INDEX2_print.php?genpage=genpage/Report201312/A11220131216%s.php&type=csv'

TWSECLS = {'01': u'水泥類股',
           '02': u'食品工業',}

def fetch_twse_list():
    with open('./twse_list.csv', 'a') as files:
        csv_file = csv.writer(files)
        re_pattern = re.compile(r'^[\d\w]{4,6}$')

        for no in TWSECLS.keys():
            for i in csv.reader(urllib2.urlopen(TWSEURL % no).readlines()):
                if re_pattern.match(i[0]):
                    csv_file.writerow([i[0], i[1].decode('cp950').encode('utf-8')])

if __name__ == '__main__':
    fetch_twse_list()
