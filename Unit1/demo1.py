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

url = 'https://movie.douban.com/explore#!type=movie&tag=%E7%A7%91%E5%B9%BB&sort=recommend&page_limit=20&page_start=0'
try:
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request, timeout=10)
    content = response.read()
    print(type(content))
    print(content.decode('utf-8'))
except urllib.error.URLError:
    print('网站错误')