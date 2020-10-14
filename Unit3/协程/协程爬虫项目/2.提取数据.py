#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 2.提取数据.py
# Author: WangYu
# Date  : 2020-09-21


from selenium import webdriver
from bs4 import BeautifulSoup
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

time.sleep(3)
driver.execute_script("javascript:goPage('2')")
print("js is  run")
time.sleep(3)
soup = BeautifulSoup(driver.page_source, 'lxml')
table = soup.find('table', attrs = {'id':'report'})
trs = table.find_all_next('tr')
name = []
d = {}
for i in trs[0].find_all('td'):
    name.append(i.text)
    d[i.text] = []
for i in trs[1:]:
    for k, val in enumerate(i.find_all('td')):
        d[name[k]].append(val.text.strip())
driver.quit()