#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 5.协程爬取阳光问政.py
# Author: WangYu
# Date  : 2020-10-04


import gevent
import gevent.monkey

gevent.monkey.patch_all()  # 自动进行切换

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import lxml
import lxml.etree


url = 'http://wz.sun0769.com/political/index/politicsNewest?id=1&page='
def geturl(start, end):
    id = []
    state = []
    title = []
    time = []
    gevent.sleep(5)
    for i in range(start, end):
        url_temp = url + str(i)
        print(url_temp)
        response = requests.get(url_temp).content.decode('utf-8')
        myxml = lxml.etree.HTML(response)
        id_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state1"]/text()')
        state_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state2"]/text()')
        title_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state3"]/a/text()')
        time_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state4"]/text()')
        for j in range(len(id_temp)):
            id_temp[j] = id_temp[j].strip()
            state_temp[j] = state_temp[j].strip()
            title_temp[j] = title_temp[j].strip()
            time_temp[j] = time_temp[j].strip()
        id.extend(id_temp)
        state.extend(state_temp)
        title.extend(title_temp)
        time.extend(time_temp)
    for k in range(len(id)):
        print(id[k], state[k], title[k], time[k])


gevent.joinall([
    gevent.spawn(geturl, 3, 6),
    gevent.spawn(geturl, 6, 9),
])