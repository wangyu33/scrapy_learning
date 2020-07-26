#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : code-encoder.py
# Author: WangYu
# Date  : 2020-07-26

import urllib.request
import urllib.parse
word = {"wd":"金"}
#编码
print(urllib.parse.urlencode(word))
#解码
print(urllib.parse.unquote(urllib.parse.urlencode(word)))

url = "http://wwww.baidu.com/s"
newurl = url + '?' + urllib.parse.urlencode(word)
print(newurl)
request = urllib.request.urlopen(newurl)
print(request.read())