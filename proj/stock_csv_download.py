#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : stock_csv_download.py
# Author: WangYu
# Date  : 2020-09-23

from urllib import request
import json
import pandas as pd

url = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh000001&scale=60&datalen=1023'


def get_data(id: str, scale=240, datalen=600):
    # 日线：scale = 240  小时：scale：60
    url_sz = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sz' \
             + str(id) + '&scale=' + str(scale) + '&datalen=' + str(datalen)
    url_sh = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=sh' \
             + str(id) + '&scale=' + str(scale) + '&datalen=' + str(datalen)
    req = request.Request(url_sh)
    rsp = request.urlopen(req)
    res = rsp.read()
    res_json = json.loads(res)
    if not res_json:
        req = request.Request(url_sz)
        rsp = request.urlopen(req)
        res = rsp.read()
        res_json = json.loads(res)

    bar_list = []

    res_json.reverse()
    for line in res_json:
        bar = {}
        bar['datetime'] = line['day']
        bar['open'] = float(line['open'])
        bar['high'] = float(line['high'])
        bar['low'] = float(line['low'])
        bar['close'] = float(line['close'])
        bar['volume'] = int(line['volume'])
        bar_list.append(bar)

    df = pd.DataFrame(data=bar_list)
    print(df)
    filename = './stock_download/' + str(id) + '.csv'
    df.to_csv(filename, index=None)


if __name__ == '__main__':
    get_data('600529')
