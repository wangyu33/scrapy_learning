#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : load_cookie.py
# Author: WangYu
# Date  : 2020-08-06

import urllib.request
from http import cookiejar

filepath = r"cookie.txt"
cookie = cookiejar.LWPCookieJar()
cookie.load(filepath, ignore_discard=False, ignore_expires=False)

header = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(header)
response = opener.open("http://www.baidu.com/")
print(response.read().decode('utf-8'))
