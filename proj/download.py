#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : download.py
# Author: WangYu
# Date  : 2020-08-18

import base64
import codecs
import json
import pickle

import random
import requests
from Crypto.Cipher import AES


def to_16(key):
    while len(key) % 16 != 0:
        key += '\0'
    return str.encode(key)


def AES_encrypt(text, key, iv):
    bs = AES.block_size
    pad2 = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    encryptor = AES.new(to_16(key), AES.MODE_CBC, to_16(iv))
    encrypt_aes = encryptor.encrypt(str.encode(pad2(text)))
    encrypt_text = str(base64.encodebytes(encrypt_aes), encoding='utf-8')
    return encrypt_text


def RSA_encrypt(text, pubKey, modulus):
    text = text[::-1]
    rs = int(codecs.encode(text.encode('utf-8'), 'hex_codec'), 16) ** int(pubKey, 16) % int(modulus, 16)
    return format(rs, 'x').zfill(256)


# 获取i值的函数，即随机生成长度为16的字符串
def get_i():
    txt = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    return ''.join(random.sample(txt, 16))


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


class WanYiYun():
    def __init__(self):
        self.url_search = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='  # post地址
        self.song_url = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token='
        self.g = '0CoJUm6Qyw8W8jud'  # buU9L(["爱心", "女孩", "惊恐", "大笑"])的值
        self.b = "010001"  # buU9L(["流泪", "强"])的值
        # buU9L(Rg4k.md)的值
        self.c = '00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.i = get_i()  # 随机生成长度为16的字符串
        self.iv = "0102030405060708"  # 偏移量
        self.headers = {'User-Agent': set_user_agent(),
                        'Referer': 'https://music.163.com/',
                        'Content-Type': 'application/x-www-form-urlencoded'
                        }

    def get_params(self, id):
        # 获取加密后的params
        if isinstance(id, int):
            # 标准 standard 较高  higher  无损lossless
            encText = {"ids": str([id]), "level": "higher", "encodeType": "aac", "csrf_token": ""}
        elif id == None:
            encText = {}
        else:
            encText = {"hlpretag": "<span class=\"s-fc7\">", "hlposttag": "</span>", "s": id, "type": "1",
                       "offset": "0",
                       "total": "true", "limit": "30", "csrf_token": ""}
        encText = json.dumps(encText)
        return AES_encrypt(AES_encrypt(encText, self.g, self.iv), self.i, self.iv)

    def get_encSecKey(self):
        # 获取加密后的encSeckey
        return RSA_encrypt(self.i, self.b, self.c)

    def get_search(self, str):
        formdata = {'params': self.get_params(str),
                    'encSecKey': self.get_encSecKey()}
        res = requests.post(self.url_search, data=formdata)
        # 获取歌曲列表的json数据
        song_info = res.json()['result']['songs']
        return song_info

    def get_download_url(self, name):
        music_list = self.get_search(name)
        cookie = pickle.load(open("wyy_cookie.pkl", "rb"))
        cookies = {}
        for c in cookie:
            cookies[c['name']] = c['value']
        cnt = 0
        words = '网易云：\n'
        for music in music_list:
            if cnt == 3:
                break
            cnt = cnt + 1
            music_id = music['id']
            # print(type(music_id))
            music_name = music['name']
            music_author = music['ar'][0]['name']
            music_album = music['al']['name']
            words = words + '歌名:' + music_name + '\n'
            words = words + '歌手:' + music_author + '\n'
            words = words + '专辑名:' + music_album + '\n'
            formdata = {'params': self.get_params(music_id),
                        'encSecKey': self.get_encSecKey()}

            response = requests.post(self.song_url, headers=self.headers, data=formdata, cookies=cookies)
            download_url = json.loads(response.content)["data"][0]["url"]
            if download_url:
                words = words + '下载链接:' + download_url + '\n'
            else:
                words = words + '下载链接:' + '无' + '\n'
        return words


if __name__ == '__main__':
    wanyiyun = WanYiYun()
    # name = input("网易云搜索关键词：")
    print(wanyiyun.get_download_url('许嵩 浅唱'))
