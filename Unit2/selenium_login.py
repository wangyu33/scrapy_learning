#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : selenium_login.py
# Author: WangYu
# Date  : 2020-09-06

import selenium
import selenium.webdriver
import time


def login_(username, password):
    drive = selenium.webdriver.Chrome()
    drive.get('https://www.douban.com/')
    time.sleep(3)
    click = drive.find_element_by_xpath('/html/body/div[1]/div[1]/ul[1]/li[2]')
    click.click()
    time.sleep(3)


login_('', '')
