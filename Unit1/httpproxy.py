#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : httpproxy.py
# Author: WangYu
# Date  : 2020-08-03

import urllib.request

httpproxy = urllib.request.ProxyHandler({"http":"14.20.235.20:808"})
opener = urllib.request.build_opener(httpproxy)
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'}
request = urllib.request.Request("http://www.baidu.com/", headers= header)
response = opener.open(request)
print(response.read().decode('utf-8'))