#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : regular_1.py
# Author: WangYu
# Date  : 2020-07-25

#正则表达式
#抓取百度搜索个数

import re
import urllib.request
import selenium
import selenium.webdriver

url = r'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=2&ch=&tn=baiduhome_pg&bar=&wd=python'

chrom_option = selenium.webdriver.ChromeOptions()
chrom_option.add_argument(r'--user-data-dir=C:\Users\wangyu\AppData\Local\Google\Chrome\User Data')
chrom_driver = r'D:\py_poj\scrapy_learning\Unit1\chromedriver.exe'
#driver = selenium.webdriver.Chrome(chrom_driver, options=chrom_option)
driver = selenium.webdriver.Chrome(chrom_driver)
driver.get(url)
pagesource = driver.page_source
mystr = pagesource
#mystr = r'<span class="nums_text">百度为您找到相关结果约74,800,000个</span>'
restr = '<span class="nums_text">百度为您找到相关结果约(.*?)个</span>'
restr = re.compile(restr,re.IGNORECASE)
num = restr.findall(mystr)[0]
num = int(num.replace(',',''))
print(num)
driver.quit()
