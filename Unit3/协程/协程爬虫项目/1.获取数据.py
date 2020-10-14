#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 1.获取数据.py
# Author: WangYu
# Date  : 2020-09-21

import requests
from pprint import pprint
import selenium
from selenium import webdriver
import time
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
driver = webdriver.Chrome(options=options, executable_path='./chromedriver')
driver.get("http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search.jsp")

time.sleep(10)
driver.execute_script("javascript:goPage('1')")
print("js is  run")
time.sleep(10)
print(driver.page_source)
driver.quit()


# def get_html_post(url, data):
#     response = requests.post(url, data)
#     return response.text
#
# def get_html_get(url):
#     response = requests.get(url)
#     return response.text
#
# post = {'yzm': 'AB4J',
#         'ft':'',
#         'ktrqks': '2020-09-21',
#         'ktrqjs': '2020-10-21',
#         'spc':'',
#         'yg':'',
#         'bg':'',
#         'ah':'',
#         'pagesnum': '1'}
# pprint(get_html_post('http://www.hshfy.sh.cn/shfy/gweb2017/ktgg_search.jsp', post))
