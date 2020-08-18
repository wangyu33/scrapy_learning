#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : get_iframe.py
# Author: WangYu
# Date  : 2020-08-15

import requests
import re
import os
from selenium import webdriver
import pandas as pd
import pickle
import time

def sleeptime(hour,min,sec):
    return hour*3600 + min*60 + sec

def get_list(url, cookie = None):
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
    options.add_argument('window-size=1600x900')  # 指定浏览器分辨率
    options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
    options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
    options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
    options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

    driver = webdriver.Chrome(options = options, executable_path='./chromedriver')

    driver.get(url)
    driver.delete_all_cookies()
    for cookie_ in cookie:
        driver.add_cookie(cookie_)
    time.sleep(3)
    driver.refresh()
    iframe_elemnt = driver.find_element_by_id("g_iframe")
    print(iframe_elemnt)
    driver.switch_to.frame(iframe_elemnt)
    #contentFrame是iframe的名称
    print(driver.page_source)

    play_list_name = driver.find_element_by_xpath('//h2[@class=\'f-ff2 f-brk\']').text
    id = []
    name = []
    author = []
    list_id = driver.find_elements_by_xpath('//tbody//tr//div[@class=\'ttc\']//span/a')
    for i in list_id:
        temp = i.get_attribute('href').replace('?','/media/outer/url?')
        temp = temp + '.mp3'
        #http://music.163.com/song/media/outer/url?id=22688491.mp3
        #音乐品质
        # http://music.163.com/api/song/detail/?id=22688491&ids=%5B22688491%5D
        print(temp)
        id.append(temp)
    list_name = driver.find_elements_by_xpath('//tbody//tr//div[@class=\'ttc\']//span//a/b')
    for i in list_name:
        name.append(i.get_attribute('title'))
    list_author = driver.find_elements_by_xpath('//tbody//tr//div[@class=\'text\']/span')
    for i in list_author:
        author.append(i.get_attribute('title'))
    dict = {'id': id, 'name': name, 'author': author}
    df = pd.DataFrame(dict, columns = ['id', 'name', 'author'])
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0'}
    for index, row in df.iterrows():
        data = requests.get(row['id'], headers=header)
        print(data.url)
        if "404" in data.url:
            df.drop(index, axis = 0,inplace = True)
            print(index)
    df.reset_index()
    path = play_list_name + '.csv'
    df.to_csv(path, index = 0)



def getcookie():
    driver = webdriver.Chrome('chromedriver.exe')
    driver.get('https://music.163.com/')
    time.sleep(30)
    cookie = driver.get_cookies()
    driver.quit()
    with open('wyy_cookie.pkl', 'wb') as f:  # db_cookie_1 为文件，不是文件夹，只需要建立一个test_cookies文件即可。
        pickle.dump(cookie, f)
    return cookie


while 1:
    if not os.path.exists('wyy_cookie.pkl'):
        getcookie()
    cookie = pickle.load(open("wyy_cookie.pkl", "rb"))
    play_list = ["https://music.163.com/#/playlist?id=468300892","https://music.163.com/#/playlist?id=466172374","https://music.163.com/#/playlist?id=466153952","https://music.163.com/#/playlist?id=491428257"]
    for list in play_list:
        get_list(list, cookie)
    time.sleep(sleeptime(24,0,0))
