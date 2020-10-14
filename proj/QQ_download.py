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


def getcookie():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://y.qq.com/')
    time.sleep(30)
    cookie = driver.get_cookies()
    driver.quit()
    with open('QQyy_cookie.pkl', 'wb') as f:
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


class QQ_Music():
    def __init__(self):
        self.get_music_url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json=1&remoteplace=txt.yqq.song&t=0&aggr=1&cr=1&w={}&format=json&platform=yqq.json'
        self.get_song_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data={"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"4095854469","songmid":["%s"],"songtype":[0],"uin":"0","loginflag":1,"platform":"20"}},"comm":{"uin":0,"format":"json","ct":24,"cv":0}}'
        self.download_url = 'http://dl.stream.qqmusic.qq.com/'
        self.headers = {'User-Agent': set_user_agent()}

    def parse_url(self, url):
        response = requests.get(url)
        return response.content.decode()

    def get_music_list(self, keyword):
        music_dirt = json.loads(self.parse_url(self.get_music_url.format(quote(keyword))))
        music_list = music_dirt['data']['song']['list']

        return music_list

    def get_download_url(self, name):
        music_list = self.get_music_list(name)
        words = 'QQ音乐：\n'
        if not os.path.exists("QQyy_cookie.pkl"):
            getcookie()
        cookie = pickle.load(open("QQyy_cookie.pkl", "rb"))
        cookies = {}
        for c in cookie:
            cookies[c['name']] = c['value']
        cnt = 0
        for music in music_list:
            # 歌手
            if cnt == 3:
                break
            cnt = cnt + 1
            music_id = music['mid']
            music_name = music['name']
            music_author = music['singer'][0]['name']
            music_album = music['album']['name']
            words = words + '歌名:' + music_name + '\n'
            words = words + '歌手:' + music_author + '\n'
            words = words + '专辑名:' + music_album + '\n'
            song_url = self.get_song_url % music_id
            response = requests.get(song_url, headers=self.headers, cookies=cookies).content
            song_dirt = json.loads(response)
            download_url = self.download_url + song_dirt["req_0"]["data"]["midurlinfo"][0]["purl"]
            if download_url != self.download_url:
                words = words + '下载链接:' + download_url + '\n'
            else:
                url = 'https://i.y.qq.com/v8/playsong.html?ADTAG=newyqq.song&songmid={}'.format(music_id)
                options = webdriver.ChromeOptions()
                options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
                options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
                options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
                options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
                options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
                options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
                mobileEmulation = {'deviceName': 'Galaxy S5'}
                options.add_experimental_option('mobileEmulation', mobileEmulation)
                driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
                driver.get(url)
                cookie = pickle.load(open("QQyy_cookie.pkl", "rb"))
                driver.delete_all_cookies()
                for cookie_ in cookie:
                    driver.add_cookie(cookie_)
                time.sleep(3)
                driver.refresh()
                response = driver.page_source
                driver.quit()
                pattern = re.compile('<audio id="h5audio_media" height="0" width="0" src="(.*?)"',
                                     re.S)
                m_url = pattern.findall(response)
                if m_url:
                    m_url[0] = m_url[0].replace(';', '&')
                    words = words + '下载链接:' + m_url[0] + '\n'
                else:
                    words = words + '下载链接:' + '无' + '\n'
        return words


if __name__ == '__main__':
    qqmusic = QQ_Music()
    print(qqmusic.get_download_url('许嵩浅唱'))
