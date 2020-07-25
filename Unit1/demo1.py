#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : demo1.py
# Author: WangYu
# Date  : 2020-07-25

import urllib.request
def download1(url):
    return urllib.request.urlopen(url).read()
def download2(url):
    return urllib.request.urlopen(url).readlines()

url = 'https://www.baidu.com/'
print(download2(url))
