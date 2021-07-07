#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 3. 问财.py
# Author: WangYu
# Date  : 2020/12/14

import pandas as pd
import requests,re,json,time,os
import tushare as ts
import os
import random
import lxml.etree
import numpy as np
import urllib.parse
import urllib.request

def set_user_agent():
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent

class wencai_select(object):
    def __init__(self, key):
        self.stock_csv = './问财.csv'
        self.url = 'http://www.iwencai.com/unifiedwap/result?'
        self.key = key
        self.headers = {'User-Agent': set_user_agent()}

    def getdata(self):
        # url = self.url + urllib.parse.urlencode(self.key)
        # /html/body/div[2]/div[4]/div[1]/div[2]/div[7]
        url = 'http://www.iwencai.com/unifiedwap/result?w=%E6%9C%BA%E6%9E%84%E6%8C%81%E8%82%A1%E5%AE%B6%E6%95%B0%3E30%E5%AE%B6%3B%E8%AF%84%E7%BA%A7%E4%B9%B0%E5%85%A5%E5%AE%B6%E6%95%B0%E4%BB%8E%E5%A4%A7%E5%88%B0%E5%B0%8F%E6%8E%92%E5%90%8D%E5%89%8D150%3Broe%3E15%25%3B%E4%B8%9A%E7%BB%A9%E5%A2%9E%E9%80%9F%E5%90%8C%E6%AF%94%E5%A2%9E%E9%95%BF%E5%A4%A7%E4%BA%8E40%25'
        response  = requests.get(url, headers = self.headers).content.decode('utf-8')
        myxml = lxml.etree.HTML(response)
        code = '/html/body/div[1]/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[4]/div[1]' \

        data = myxml.xpath(code)



        print(1)



key = {'w':'机构持股家数>30家;评级买入家数从大到小排名前150;roe>15%;业绩增速同比增长大于40%'}
a = wencai_select(key)
b = a.getdata()
# print(urllib.parse.urlencode(key))