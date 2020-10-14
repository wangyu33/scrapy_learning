#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : stock.py
# Author: WangYu
# Date  : 2020-09-15

import requests
from pprint import pprint
from bs4 import BeautifulSoup
import random
import re
import pandas as pd
import urllib
from lxml import etree
import os
import math
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


class stock:
    def __init__(self):
        self.industry_url = 'https://www.holdle.com/stocks/industry?'
        self.get_stock_url = 'https://www.holdle.com/stocks/industry?order='
        self.headers = {'User-Agent': set_user_agent()}
        self.industry = self.get_industry()

    def get_industry(self):
        response = requests.get(self.industry_url, headers = self.headers).content
        soup = BeautifulSoup(response, 'lxml')
        l = []
        for link in soup.find_all('a'):
            if 'href' in link.attrs:
                if len(link.attrs) == 1 and 'order' in link.attrs['href']:
                    temp = link.text
                    l.append(temp)
        l.remove('A 股')
        l.remove('美股')
        industry_list = l[:]
        for i, temp in enumerate(l):
            industry_list[i] = industry_list[i].replace('\n', '')
            for k in range(10):
                industry_list[i] = industry_list[i].replace(str(k), '')
        return industry_list

    def get_stock(self):
        for industry in self.industry:
            industry_url = self.get_stock_url + urllib.parse.quote(industry)
            content = requests.get(industry_url, headers = self.headers).text
            content = etree.HTML(content)
            stock_id = content.xpath('/html/body/div[1]/div/div[3]/div[2]/div')
            csv = []
            for num, block in enumerate(stock_id):
                table = block.xpath('table/tr/td/text()')
                table_name = table[0]
                name = []
                value = []
                for i, temp in enumerate(table[1:]):
                    if i%2 == 0:
                        name.append(str(temp))
                    else:
                        value.append(str(temp))
                id = block.xpath('table/tr/@class')[1:]
                id = [str(temp).replace('stock-', '') for temp in id]
                data = {'name': name, 'id': id, table_name + ' value': value}
                table_name = table_name.replace('/', '除')
                if num == 0:
                    csv = pd.DataFrame(data)
                elif num < 5:
                    csv_temp = pd.DataFrame(data)
                    csv = pd.merge(csv, csv_temp, on = ['id', 'name'], how = 'outer')
                elif num == 5:
                    csv_temp = pd.DataFrame(data)
                    csv = pd.merge(csv, csv_temp, on = ['id', 'name'], how = 'outer')
                    csv.to_csv('./stock/' + industry + '.csv', encoding = 'utf_8_sig', index = False)
                    print(industry + ' is complete!')

    def stock_pool(self):
        path = './stock/'
        theta = 0.2
        stock_pool = {'name': [], 'id': [], 'industry': []}
        for file in os.listdir(path):
            file_name = path + file
            df = pd.read_csv(file_name, dtype = {'id': str})
            df = df.fillna(0)
            size = len(df['name'])
            col_name = df.columns.values
            for att in col_name:
                if att == 'name' or att == 'id':
                    continue
                df[att] = df[att] / max(df[att])
            score = 1 * df[col_name[2]] + 1 * df[col_name[3]] + 0.4 * df[col_name[4]] \
                   + 0.4 * df[col_name[5]] + 0.6 * df[col_name[6]] + 0.1 * df[col_name[7]]
            data = {'name': df['name'], 'id': df['id'], 'score': score}
            df = pd.DataFrame(data)
            df = df.sort_values(['score'], ascending = False).reset_index(drop = True).head(math.ceil(size * theta))
            stock_pool['name'].extend(list(df['name'].values))
            stock_pool['id'].extend(list(df['id'].values))
            industry = file[:-4]
            industry = [industry] * math.ceil(size * theta)
            stock_pool['industry'].extend(industry)
            print(file[:-4] + 'is complete')

        df = pd.DataFrame(stock_pool)
        df.to_csv('./stock_pool.csv', encoding = 'utf_8_sig', index = False)





temp = stock()
temp.stock_pool()