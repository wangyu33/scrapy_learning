#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : tianya.py
# Author: WangYu
# Date  : 2020/12/2

import scrapy
import re  # 正则表达式
import sys
sys.path.append("..")
import items

# 下载数据
class TianyaSpider(scrapy.Spider):
    name = 'tianya'
    allowed_domains = ['tianya.com']
    start_urls = ['http://bbs.tianya.cn/post-140-393977-1.shtml']

    def parse(self, response):
        savefile = open("tianya.html", "w")
        pagedata = response.body.decode("gbk", "ignore")
        savefile.write(pagedata)
        savefile.close()

        regex = re.compile(r"([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})", re.IGNORECASE)  # 预编译正则
        maillist = regex.findall(pagedata)

        for mail in maillist:
            myitem = items.EmailSpiderItem()
            myitem["email"] = mail
            myitem["url"] = "http://bbs.tianya.cn/post-140-393977-1.shtml"
            yield myitem
