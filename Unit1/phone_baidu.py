#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : phone_baidu.py
# Author: WangYu
# Date  : 2020-07-26

import urllib.request
def  downloadasAndroid(url):
    #header={"Android QQ":"User-Agent: MQQBrowser/26 Mozilla/5.0 (Linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"}
    header = {"UC": "User-Agent: UCWEB7.0.2.37/28/999"}
    request=urllib.request.Request(url,headers=header)
    #request.add_header("Connection","keep-live")
    print(request.get_full_url()) #整个网页链接
    print(request.host) #服务器域名
    print(request.get_method()) #get 或者post
    print(request.type) #http或者ftp,https
    response = urllib.request.urlopen(request)
    print(response.code) #200,404,403,编号
    print(response.info()) #网页详细信息
    content = response.read()
    print(content.decode('utf-8')) #网页源代码


downloadasAndroid("https://www.baidu.com")