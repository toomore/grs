
Quick Start
===========

擷取上市股價資訊
-----------------------------

::

    from grs import Stock

    stock = Stock('2618')                         # 擷取長榮航股價
    print stock.moving_average(5)                 # 計算五日均價與持續天數
    print stock.moving_average_value(5)           # 計算五日均量與持續天數
    print stock.moving_average_bias_ratio(5, 10)  # 計算五日、十日乖離值與持續天數


擷取 12 個月份資料
-----------------------------

::

    stock = Stock('2618', 12)


輸出 CSV 檔
-----------------------------

::

    stock.out_putfile('/dev/shm/2618.csv')


擷取上櫃股價資訊
-----------------------------

::

    from grs import Stock

    stock = Stock('8446')                         # 擷取華研股價
    print stock.moving_average(5)                 # 計算五日均價與持續天數
    print stock.moving_average_value(5)           # 計算五日均量與持續天數
    print stock.moving_average_bias_ratio(5, 10)  # 計算五日、十日乖離值與持續天數


如果已確定該代碼為上市或上櫃股票，可以直接指定參數跳過查表動作。

::

    stock = Stock('2618', twse=True) # 擷取長榮航股價
    stock = Stock('8446', otc=True)  # 擷取華研股價


.. seealso:: :doc:`fetch_data`

顯示台灣時間：TWTime
-----------------------------

適用於其他時區查詢台灣當地時間。

::

    from grs import TWTime

    what_time = TWTime()
    what_time.now()        # 顯示台灣此刻時間
    what_time.localtime()  # 顯示當地此刻時間

.. seealso:: :doc:`tw_time`

判斷台灣股市是否開市：TWSEOpen
----------------------------------

::

    from grs import TWSEOpen
    from datetime import datetime

    open_or_not = TWSEOpen()

    open_or_not.d_day(datetime.today())        # 判斷今天是否開市
                                               # 回傳 True or False
    open_or_not.d_day(datetime(2012, 12, 22))  # 判斷 2012/12/22 是否開市

.. seealso:: :doc:`twseopen`


各股即時盤資訊：RealtimeTWSE / RealtimeOTC
---------------------------------------------

上市即時資訊

::

    from grs import RealtimeTWSE

    realtime_stock = RealtimeTWSE('2618')   # 擷取長榮航即時股價
    realtime_stock.raw                      # 原始資料
    realtime_stock.data                     # 回傳 type: dict


上櫃即時資訊

::

    from grs import RealtimeOTC

    realtime_stock = RealtimeOTC('8446')    # 擷取華研即時股價
    realtime_stock.raw                      # 原始資料
    realtime_stock.data                     # 回傳 type: dict

.. seealso:: :doc:`realtime`

大盤即時盤資訊：RealtimeWeight（加權指數、櫃檯指數、寶島指數）
---------------------------------------------------------------

::

    from grs import RealtimeWeight

    realtime_weight = RealtimeWeight()  # 擷取即時大盤資訊
    realtime_weight.raw                 # 原始檔案
    realtime_weight.data                # 回傳 type: dict

.. seealso:: :doc:`realtime`


上市股票代碼列表：TWSENo
-----------------------------

回傳上市股票代碼與搜尋

::

    from grs import TWSENo


    twse_no = TWSENo()
    twse_no.all_stock       # 所有股票名稱、代碼 type: dict
    twse_no.all_stock_no    # 所有股票代碼 type: list
    twse_no.all_stock_name  # 所有股票名稱 type: list
    twse_no.industry_code   # 回傳類別代碼 type: dict
    twse_no.industry_comps  # 回傳類別所屬股票代碼 type: dict
    twse_no.search(u'中')   # 搜尋股票名稱，回傳 type: dict
    twse_no.searchbyno(23)  # 搜尋股票代碼，回傳 type: dict
    twse_no.last_update     # 回傳列表最後更新時間（非同步）type: str

.. seealso:: :doc:`twseno`

單日倒數時間：Countdown
-----------------------------

適用於設定 cache 時間。

::

    from grs import Countdown

    countdown = Countdown(hour=14, minutes=30)  # 預設為 14:30
    countdown.nextday    # 下一個 14:30 日期
    countdown.countdown  # 到數秒數
    countdown.exptime    # 下一個 14:30 日期時間（type: datetime）
    countdown.lastmod    # 前一個 14:30 日期時間（type: datetime）

.. seealso:: :doc:`tw_time`

判斷乖離轉折點：Stock(no).check_moving_average_bias_ratio
------------------------------------------------------------------

判斷乖離轉折點

::

    from grs import Stock

    stock = Stock('2618')
    data = stock.moving_average_bias_ratio(3, 6)[0]  # 取得 3-6 乖離值 type: list

    # 計算五個區間負乖離轉折點
    check_data = stock.check_moving_average_bias_ratio(data, sample=5,
                                                    positive_or_negative= False)
    print check_data  # (T/F, 第幾轉折日, 乖離轉折點值) type: tuple

.. seealso:: :doc:`fetch_data`

四大買賣點判斷：BestFourPoint
----------------------------------

判斷是否為技術分析的四大買賣點，條件成立，回傳條件結果，判斷結果僅供參考！

::

    from grs import BestFourPoint
    from grs import Stock

    stock = Stock('2618')
    result = BestFourPoint(stock)
    result.best_four_point_to_buy()       # 判斷是否為四大買點
    result.best_four_point_to_sell()      # 判斷是否為四大賣點
    result.best_four_point()              # 綜合判斷

全部上市股票檢視

::

    from grs import BestFourPoint
    from grs import Stock
    from grs import TWSENo

    stock_no_list = TWSENo().all_stock_no

    for i in stock_no_list:
        try:
            best_point, info = BestFourPoint(Stock(i)).best_four_point()
            if best_point:  # 買點
                print 'Buy: {0} {1}'.format(i, info)
            else:   # 賣點
                print 'Sell: {0} {1}'.format(i, info)
        except:     # 不作為或資料不足
            print 'X: {0}'.format(i)

.. seealso:: :doc:`best_buy_or_sell`

擴充月份資料：Stock(no).plus_mons(month)
-----------------------------------------------

當原有的月份資料不夠時，不需要從頭抓取，只需要給予增額月份值即可。

::

    from grs import Stock

    stock = Stock('2618')                # 預設為抓取３個月份資料
    stock.moving_average(60)
    IndexError: list index out of range  # 資料不足
    len(stock.raw)                       # 回傳 51 個值
    stock.plus_mons(1)                   # 在抓取一個月資料
    len(stock.raw)                       # 回傳 66 個值
    stock.moving_average(60)             # 計算成功

.. seealso:: :doc:`fetch_data`
