#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : QQ_download.py
# Author: WangYu
# Date  : 2020-08-18

import os, json
import re
from selenium import webdriver
from urllib.parse import quote
import time
import requests
import pickle
import random
import lxml
import lxml.etree


def getcookie():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://music.hwkxk.cf/')
    time.sleep(30)
    cookie = driver.get_cookies()
    driver.quit()
    with open('music_cookie.pkl', 'wb') as f:
        pickle.dump(cookie, f)
    return cookie




def set_user_agent():
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent


class Music():
    def __init__(self):
        self.url = 'https://music.hwkxk.cf/?kw='
        self.headers = {'User-Agent': set_user_agent()}

    def regeturl(self, url, cookies):
        response = requests.get(url, headers=self.headers, cookies = cookies)
        return response.url

    def get_download_url(self, name, source = 'kuwo'):
        url = self.url + quote(name) + '&source=' + source
        if not os.path.exists("music_cookie.pkl"):
            getcookie()
        cookie = pickle.load(open("music_cookie.pkl", "rb"))
        cookies = {}
        for c in cookie:
            cookies[c['name']] = c['value']
        response = requests.get(url, headers=self.headers, cookies=cookies).content.decode('utf-8')
        myxml = lxml.etree.HTML(response)
        song_list = myxml.xpath('/html/body/div/div[1]/table/tr')
        words = source + '音乐：\n'
        cnt = 0
        for song in song_list[1:]:
            if cnt == 1:
                break
            cnt += 1
            name = song.xpath('td[1]/text()')
            stard = song.xpath('td[2]/a[1]/@href')
            # high = song.xpath('td[2]/a[2]/@href')
            # lossless = song.xpath('td[2]/a[3]/@href')
            if name:
                words = words + '歌名:' + name[0] + '\n'
            if stard:
                words = words + '标准:' + self.regeturl(stard[0], cookies) + '\n'
            # if high:
            #     words = words + '高品质:' + self.regeturl(high[0], cookies) + '\n'
            # if lossless:
            #     words = words + '无损:' + self.regeturl(lossless[0], cookies) + '\n'
        return words



if __name__ == '__main__':
    m = Music()
    print(m.get_download_url('浅唱'))
