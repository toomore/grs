.. grs documentation master file, created by
   sphinx-quickstart on Thu Jan 16 00:58:25 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to grs's documentation!
===============================

============================
grs 台灣上市股票價格擷取
============================

.. image:: https://secure.travis-ci.org/toomore/grs.png
   :target: http://travis-ci.org/toomore/grs

.. image:: https://pypip.in/d/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

.. image:: https://pypip.in/v/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

.. image:: https://pypip.in/wheel/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

.. image:: https://pypip.in/license/grs/badge.png
   :target: https://pypi.python.org/pypi/grs

主要開發擷取台灣股市（TWSE）股價資料，資料來源 `證券交易所網站 <http://www.twse.com.tw/>`_ 。

版本資訊
-----------------------------

:Authors: Toomore Chiang
:Version: 0.4.2 of 2014/01/11
:Python Version: Python 2.7, PyPy

Requires
-----------------------------

- python-dateutil==1.5

Report Issue or get involved
-----------------------------

- Github → https://github.com/toomore/grs
- Issues → https://github.com/toomore/grs/issues

Web Demo
-----------------------------

- grs Online → http://grs.toomore.net/

Quick start
------------

.. toctree::
   :maxdepth: 2

   quick-start

Feature
-----------

.. toctree::
   :maxdepth: 2

   擷取股票資訊 grs.Stock <fetch_data>
   上市股票列表 grs.TWSENo <twseno>
   判斷是否開市 grs.TWSEOpen <twseopen>
   時間、倒數處理 grs.TWTime/Countdown <tw_time>
   四大買賣點判斷 grs.BestFourPoint <best_buy_or_sell>


Change Logs
-----------------------------

* 0.4.2 2014/01/11
    - 修正：Stock ``stock_no``, RealtimeStock ``no`` 必須為 *string*.
      `Issues #9 <https://github.com/toomore/grs/issues/9>`_

* 0.4.1 2014/01/02
    - 修正：Countdown().countdown 秒數問題
    - 新增：twse_no, twse_open, twse_realtime, countdown into unittest
    - 移除：Support Python 2.6

* 0.4.0 2013/12/30
    - 修正：Naming Convention
    - 修正：Coding style to fit PEP8
    - 新增：For PyPy

* 0.3.0 2013/12/18
    - 更新：股票代碼列表
    - 更新：2014 年集中交易市場開（休）市日期表

* 0.2.1 2013/12/16
    - 修正：部分資料改用 tuple

* 0.2.0 2012/04/13
    - 修正：輸出中文統一使用 Unicode
    - 修正：需要套件 python-dateutil 調整為 1.5
    - 修正：Web Demo 網站網址
    - 新增：Stock.plusMons() 擴充月份資料

* 0.1.4 2012/04/01
    - 修正：每月首日無資料抓取問題

* 0.1.3 2012/03/31
    - 修正：Countdown 倒數時間計算錯誤（dateutil.relativedelta）

* 0.1.2 2012/03/31
    - 修正：grs 倒數時間計算錯誤（dateutil.relativedelta）

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

