#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : cookie.py
# Author: WangYu
# Date  : 2020-08-03

#进入网站的debug模式

import urllib.request

httphander = urllib.request.HTTPHandler(debuglevel=1)
httpshander = urllib.request.HTTPSHandler(debuglevel=1) #访问网络输出调试信息

opener = urllib.request.build_opener(httphander,httpshander)
urllib.request.install_opener(opener)

urllib.request.urlopen("http://www.renren.com")

#读取cookie
from http import cookiejar

cookie = cookiejar.CookieJar()
header = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(header)
response = opener.open("http://www.baidu.com")
cookies = ""
for data in cookie:
    cookies = cookies + data.name + "=" + data.value + ";\r\n"
print(cookies)