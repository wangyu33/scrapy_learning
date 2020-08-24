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
import urllib.request,os,json
from lxml import etree
from requests_html import HTMLSession
import execjs,requests,random
import base64,codecs
from Crypto.Cipher import AES

header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}

play_list = ["https://music.163.com/#/playlist?id=468300892","https://music.163.com/#/playlist?id=466172374","https://music.163.com/#/playlist?id=466153952","https://music.163.com/#/playlist?id=491428257"]

session = HTMLSession()
response = session.get(play_list[0])
html = etree.HTML(response.content.decode())
print(1)


