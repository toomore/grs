#!/usr/bin/env python
# -*- coding: utf-8 -*-

import grs
from setuptools import setup, find_packages

long_description = open('./README.rst', 'r').read()
description = '台灣上市上櫃股票價格擷取（Fetch Taiwan Stock Exchange data）' + \
              '含即時盤、台灣時間轉換、開休市判斷。'

setup(name='grs',
      version=grs.__version__,
      description=description,
      long_description=long_description,
      author=grs.__author__,
      author_email='toomore0929@gmail.com',
      url='https://github.com/toomore/grs',
      packages=['grs'],
      package_data={'grs': ['*.csv']},
      include_package_data=True,
      license=grs.__license__,
      keywords="Taiwan Stock Exchange taipei twse otc gretai " + \
               "台灣 台北 股市 即時 上市 上櫃",
      install_requires=['python-dateutil==1.5', 'ujson', 'urllib3'],
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Financial and Insurance Industry',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: MIT License',
          'Natural Language :: Chinese (Traditional)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Office/Business :: Financial :: Investment',
          ],
     )
