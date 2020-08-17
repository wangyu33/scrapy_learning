#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : music.py
# Author: WangYu
# Date  : 2020-08-09

#用于爬取网易云歌单

import requests
import re
import time
import os
from selenium import webdriver
def getcookie():
    if os.path.exists('./WYY_cookies.txt') == False:
        driver = webdriver.Chrome('chromedriver.exe')
        driver.get('https://music.163.com/#/playlist?id=468300892')
        global session
        time.sleep(60)
        print(driver.page_source)
        with open(r'./WYY_cookies.txt', 'w+') as f:
            print("write cookies")
            for cookie in driver.get_cookies():
                f.write(cookie['name'] + '==' + cookie['value'] + '\n')
        f.close()

    with open(r'./WYY_cookies.txt', 'r') as f:
        ans = f.readlines()
    cookies = {}
    for an in ans:
        an = an.replace('\n', '')
        a = an.split('==')
        cookies[a[0]] = a[1]
    return cookies

cookie = getcookie()
print(type(cookie))
for k in cookie:
    print(k)
    print(cookie[k])

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

play_list = ["https://music.163.com/#/playlist?id=468300892","https://music.163.com/#/playlist?id=466172374","https://music.163.com/#/playlist?id=466153952","https://music.163.com/#/playlist?id=491428257"]
play_list_name = []



str = "<a href=\"/song?id=(\d+)\">"
for url in play_list:
    data = requests.get(url, headers = header, cookies = cookie).content.decode('utf-8')
    print(data)
    temp = re.findall(str, data)
    play_list_name.append(1)
    print(play_list_name)

# data = requests.get(url, headers = header)
# if "404" in data.url:
#     print("--------------")