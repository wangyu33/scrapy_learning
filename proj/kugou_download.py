#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : kugou_download.py
# Author: WangYu
# Date  : 2020-08-18

from requests_html import HTMLSession
import urllib.request,os,json
from urllib.parse import quote
class KuGou():
    def __init__(self):
        self.get_music_url='https://songsearch.kugou.com/song_search_v2?keyword={}&platform=WebFilter'
        self.get_song_url='https://wwwapi.kugou.com/yy/index.php?r=play/getdata&hash={}'
        if not os.path.exists("d:/music"):
            os.mkdir('d:/music')

    def parse_url(self,url):
        session = HTMLSession()
        response = session.get(url)
        return response.content.decode()

    def get_music_list(self,keyword):
        music_dirt=json.loads(self.parse_url(self.get_music_url.format(quote(keyword))))
        music_list=music_dirt['data']['lists']
        song_list=[]
        for music in music_list:
            song_name=music['FileName'].replace("<\\/em>", "").replace("<em>", "")
            song_list.append({'hash':music['FileHash'], 'song_name':song_name})
            print(str(len(song_list))+'---'+song_name)
        return song_list

    def download(self,song):
        song_dirt=json.loads(self.parse_url(self.get_song_url.format(song['hash'])))
        download_url=song_dirt['data']['play_url']
        if download_url:
            try:
                # 根据音乐url地址，用urllib.request.retrieve直接将远程数据下载到本地
                urllib.request.urlretrieve(download_url, 'd:/music/' + song['song_name'] + '.mp3')
                print('Successfully Download:' + song['song_name'] + '.mp3')
            except:
                print('Download wrong~')

if __name__ == '__main__':
    kugou=KuGou()
    while True:
        keyword=input('请输入要下载的歌曲名：')
        print('-----------歌曲《'+keyword+'》的版本列表------------')
        music_list=kugou.get_music_list(keyword)
        song_num=input('请输入要下载的歌曲序号：')
        kugou.download(music_list[int(song_num)-1])