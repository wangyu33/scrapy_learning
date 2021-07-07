#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 勾画复选框.py
# Author: WangYu
# Date  : 2020/11/20

import time

from selenium import webdriver

# 指定驱动

driver = webdriver.Chrome(r"./chromedriver.exe")

# 打开网址

driver.get('https://www.ncbi.nlm.nih.gov/pccompound?LinkName=pcassay_pccompound_inactive&from_uid=2316')
time.sleep(10)


while 1:
    input1 = driver.find_elements_by_xpath('/html/body/div[1]/div[1]/form/div[1]/div[4]/div/div[5]/div/div[1]/input')

    # 判断是否已经选中

    if input1:  # 判断是否有找到元素
        for checkbox in input1:  # 循环点击找到的元素
            checkbox.click()  # 勾选复选框
            # time.sleep(2)
    else:
        print("没有找到元素")

    time.sleep(10)

