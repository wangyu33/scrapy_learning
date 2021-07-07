#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 2. 选股.py
# Author: WangYu
# Date  : 2020/11/5

import pandas as pd
import requests,re,json,time,os
import tushare as ts
import os
import random
import lxml.etree
import numpy as np


def set_user_agent():
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent

class stock_select(object):
    def __init__(self):
        self.stock_csv = './stocks.csv'
        self.stock_code = self.getcode().code.values
        self.headers = {'User-Agent': set_user_agent()}

    def getStock(self):
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

    def getcode(self):
        if os.path.exists(self.stock_csv):
            data = pd.read_csv(self.stock_csv, index_col=False)
            # return data
        else:
            self.getStock()
            data = pd.read_csv(self.stock_csv, index_col=False)
            # return data
        code = []
        for i in data.iterrows():
            temp = i[1]
            code_temp = '0' * (6-len(str(temp[0]))) + str(temp[0])
            code.append(code_temp)
        data['code'] = code
        return data

    def getdata(self, code):
        # url = 'https://xueqiu.com/S/' + 'SZ' + code
        url = 'http://quotes.money.163.com/f10/zycwzb_' + code + '.html'
        # /html/body/div[2]/div[4]/div[1]/div[2]/div[7]
        response  = requests.get(url, headers = self.headers).content.decode('utf-8')
        myxml = lxml.etree.HTML(response)
        col_l = myxml.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/div[7]/table/tbody/tr/td/text()')
        time = myxml.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/div[8]/table/tr[1]/th/text()')
        data = myxml.xpath('/html/body/div[2]/div[4]/div[1]/div[2]/div[8]/table/tr[position()>1]/td/text()')
        data = np.array(data)
        data = data.reshape(len(col_l),-1)
        data = list(data)
        dict = {}
        for index, atr in enumerate(col_l):
            dict[atr] = list(data[index][0:6])
        data2 = myxml.xpath('/html/body/div[2]/div[4]/div[3]/div[4]/table/tr[position()>1]/td/text()')
        data2 = np.array(data2)
        data2 = data2.reshape(-1, 7)
        col_l = list(data2[:, 0])
        data2 = data2[:, 1:]
        data2 = list(data2)
        for index, atr in enumerate(col_l):
            dict[atr] = list(data2[index])
        df = pd.DataFrame(dict, index = time[0:6])


        print(1)




a = stock_select()
b = a.getdata('000001')
