#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

long_description = open('./README.rest', 'r').read()
description = '台灣上市股票價格擷取（Fetch TWSE stock data）' + \
              '含即時盤、台灣時間轉換、開休市判斷。'

setup(name='grs',
      version='0.1.4',
      description=description,
      long_description=long_description,
      author='Toomore Chiang',
      author_email='toomore0929@gmail.com',
      url='https://github.com/toomore/grs',
      packages=['grs'],
      include_package_data=True,
      license='MIT',
      keywords="stock taiwan taipei twse 台灣 股市 台北 即時",
      install_requires=['python-dateutil==2.1'],
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
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Topic :: Office/Business :: Financial :: Investment',
          ],
     )
