#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : Redirect.py
# Author: WangYu
# Date  : 2020-08-03

#识别网页是否重定向

import urllib.request
import re

response = urllib.request.urlopen("http://www.baidu.cn")
content = response.read().decode('utf-8')
print(content)
str = 'url=(.*)">'
restr = re.compile(str,re.IGNORECASE)
print(restr.findall(content)[0])
