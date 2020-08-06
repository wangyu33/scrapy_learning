#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : save_cookie.py
# Author: WangYu
# Date  : 2020-08-06

import urllib.request
from http import cookiejar

filepath = "cookie.txt"
cookie = cookiejar.LWPCookieJar(filepath)
header = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(header)
response = opener.open("http://www.baidu.com")

cookie.save(ignore_expires=True, ignore_discard=True)