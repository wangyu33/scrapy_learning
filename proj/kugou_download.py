#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : kugou_download.py
# Author: WangYu
# Date  : 2020-08-18

import urllib.request,os,json
from urllib.parse import quote
import random
import requests
import time
from selenium import webdriver
import hashlib

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

class KuGou():
    def __init__(self):
        self.get_music_url='https://songsearch.kugou.com/song_search_v2?keyword={}&platform=WebFilter'
        self.get_song_url='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'
        self.headers = {'User-Agent': set_user_agent()}

    def parse_url(self,url):
        response = requests.get(url,headers = self.headers)
        return response.content.decode()

    def get_music_list(self,keyword):
        url = self.get_music_url.format(quote(keyword))
        music_dirt = json.loads(self.parse_url(url))
        music_list = music_dirt['data']['lists']
        return music_list

    def creat_mid(self):
        md5 = hashlib.md5()
        # 随机生成4位随机的字符列表 范围为a-z 0-9
        n = random.sample('abcdefghijklmnopqrstuvwxyz0123456789', 4)
        # 将列表元素拼接为字符串
        n = ''.join(n)
        # 将字符串编码后更新到md5对象里面
        md5.update(n.encode())
        # 调用hexdigest获取加密后的返回值
        result = md5.hexdigest()
        return result

    def get_download_url(self, key):
        music_list = self.get_music_list(key)
        cnt = 0
        words = '酷狗：\n'
        for music in music_list:
            if cnt == 3:
                break
            cnt = cnt + 1
            music_id = music['FileHash']
            # print(type(music_id))
            music_name = music['SongName']
            music_author = music['SingerName']
            music_album = music['AlbumName']
            words = words + '专辑名:' + music_album + '\n'
            words = words + '歌名:' + music_name + '\n'
            words = words + '歌手:' + music_author + '\n'
            song_url = self.get_song_url.format(music_id) + '&mid=' + self.creat_mid()
            response = json.loads(requests.get(song_url, headers = self.headers).content.decode())

            download_url = response['data']['play_url']
            if download_url:
                words = words + '下载链接:' + download_url + '\n'
            else:
                words = words + '下载链接:' + '无' + '\n'
        return words

if __name__ == '__main__':
    kugou=KuGou()
    print(kugou.get_download_url('许嵩浅唱'))