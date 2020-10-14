#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 3.阳光问政多线程锁.py
# Author: WangYu
# Date  : 2020-10-08

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import lxml
import lxml.etree
import threading

url = 'http://wz.sun0769.com/political/index/politicsNewest?id=1&page='


def geturl(start, end, file):
    id = []
    state = []
    title = []
    time = []
    for i in range(start, end):
        url_temp = url + str(i)
        # print(url_temp)
        response = requests.get(url_temp).content.decode('utf-8')
        myxml = lxml.etree.HTML(response)
        id_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state1"]/text()')
        state_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state2"]/text()')
        title_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state3"]/a/text()')
        time_temp = myxml.xpath('/html/body/div[2]/div[3]/ul[2]/li//span[@class="state4"]/text()')
        mygetstr = ""
        for j in range(len(id_temp)):
            id_temp[j] = id_temp[j].strip()
            state_temp[j] = state_temp[j].strip()
            title_temp[j] = title_temp[j].strip()
            time_temp[j] = time_temp[j].strip()

            mygetstr += id_temp[j]
            mygetstr += " # "
            mygetstr += state_temp[j]
            mygetstr += " # "
            mygetstr += title_temp[j]
            mygetstr += " # "
            mygetstr += time_temp[j]
            mygetstr += "\r\n"  # 换行
            print(mygetstr)
            with  rlock:
                file.write(mygetstr.encode("utf-8", errors="ignore"))

rlock = threading.RLock()#避免冲突
file=open("morethread.txt","wb")
threadlist = []
for i in range(10):
    mythread = threading.Thread(target=geturl, args=(i * 10 + 1, i * 10 + 9, file))
    mythread.start()
    threadlist.append(mythread)

for thd in threadlist:
    thd.join()