#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 1.baidu_ocr.py
# Author: WangYu
# Date  : 2020-10-18

# encoding:utf-8

import requests
import base64

'''
通用文字识别
'''


# client_id 为官网获取的AK， client_secret 为官网获取的SK
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=XdSXDGVwHZfo2Q9AXjmxdTvi&client_secret=TmpKG1mXEt6ad3cEV5ufeHVDfvI2fIjT'
response = requests.get(host)
if response:
    # print(response.json())
    response = response.json()


request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
# 二进制方式打开图片文件
f = open('1.jpg', 'rb')
img = base64.b64encode(f.read())

params = {"image":img}
access_token = response['access_token']
request_url = request_url + "?access_token=" + access_token
headers = {'content-type': 'application/x-www-form-urlencoded'}
response = requests.post(request_url, data=params, headers=headers)
if response:
    print(response.json())