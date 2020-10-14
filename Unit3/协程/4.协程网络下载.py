#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 4.协程网络下载.py
# Author: WangYu
# Date  : 2020-09-17

import gevent
import gevent.monkey
gevent.monkey.patch_all()  # 自动进行切换

import requests

def download(url):
    print('start', url)
    data = requests.get(url).content
    print(url, ' \'s len', len(data))


gevent.joinall([
    gevent.spawn(download, 'https://www.baidu.com/'),
    gevent.spawn(download, 'https://www.163.com/'),
    gevent.spawn(download, 'https://www.qq.com/')
])
