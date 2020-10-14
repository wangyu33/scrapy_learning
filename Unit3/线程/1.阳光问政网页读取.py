#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 1.阳光问政网页读取.py
# Author: WangYu
# Date  : 2020-10-04

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import lxml
import lxml.etree

def geturl(url):
    for i in range(1,2):
        url_temp = url + str(i)
        response = requests.get(url_temp).content.decode('utf-8')
        myxml = lxml.etree.HTML(response)
        id = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state1"]/text()')
        state = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state2"]/text()')
        title = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state3"]/a/text()')
        time = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state4"]/text()')
        for j in range(len(id)):
            id[j] = id[j].strip()
            state[j] = state[j].strip()
            title[j] = title[j].strip()
            time[j] = time[j].strip()
        print(1)

url = 'http://wz.sun0769.com/political/index/politicsNewest?id=1&page='
geturl(url)