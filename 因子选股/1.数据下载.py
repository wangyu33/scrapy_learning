#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 1.数据下载.py
# Author: WangYu
# Date  : 2020-10-19


import backtrader as bt
import backtrader.indicators as bi
import pandas as pd
import tushare as ts




# 获取股票数据，进行初步筛选，返回供因子分析的股票数据。
def getFactors():
    data = ts.get_stock_basics()
    # 排除亏损的股票
    data = data[data.npr > 0.0]
    # 排除上市不满2年的
    # data = data[data.timeToMarket <= 20180801]
    data = data[data.pe <= 200]
    # 排除ST股票
    data = data[~ data.name.str.contains("ST")]
    # print(data)
    data = data.sort_values(by = 'industry')
    data.to_csv("stocks.csv")
    print(set(data.industry))
    return data


if __name__ == "__main__":
    factors = getFactors()
# 分析数据
def analysis(factors):
    print("平均市盈率:%.2f" % (factors.pe.mean()))
    print("每股收益:%.2f" % (factors.esp.mean()))
    print("每股净资产:%.2f" % (factors.bvps.mean()))
    print("平均市净率:%.2f" % (factors.pb.mean()))
    print("平均每股净利润:%.2f" % (factors.npr.mean()))
    print("平均股东人数:%.2f" % (factors.holders.mean()))