#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : demo1.py
# Author: WangYu
# Date  : 2020-07-25

import urllib.request
import urllib.error
def download1(url):
    return urllib.request.urlopen(url).read()
def download2(url):
    return urllib.request.urlopen(url).readlines()

url = 'https://www.baidu.com/'
try:
    response = urllib.request.urlopen(url, timeout=10)
    print(response.info)
    print(download2(url))
except urllib.error.URLError:
    print('网站错误')