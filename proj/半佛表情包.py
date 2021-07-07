#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 半佛表情包.py
# Author: WangYu
# Date  : 2020/12/15

import requests
import time
import json
import csv
import random
from bs4 import BeautifulSoup
import re
import os
from tqdm import tqdm
from requests.packages.urllib3.exceptions import InsecureRequestWarning, InsecurePlatformWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)

"""
本项目首发：
B站原创视频：https://www.bilibili.com/video/BV1Vz41187Rt
公众号原创文章：https://mp.weixin.qq.com/s/fVDwNdVDZo_0q6jAMWCGAA
公众号：Python知识圈（id：PythonCircle）
哔哩哔哩：菜鸟程序员的日常
"""


def request_data():
    article_url_list = []
    print('正在下载，请稍等！大约需要30分钟')
    for offset in tqdm(range(0, 300, 10)):
        # 记得把offset后面的值改成{}
        base_url = 'http://mp.weixin.qq.com/mp/profile_ext?offset={}&count=10'

        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行
        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行
        # 下面的值以自己的为准，部分省略了，从转换工具里复制过来就行

        cookies = {
            'devicetype': 'android-28',
            'lang': 'zh_CN',
            'pass_ticket': '7sVse3N83I76nZYVGdoQvcT3Y2brTifoLiQm8WTqP0P83kvp5riUoNNF2N1eg6',
            'version': '27001539',
        }

        headers = {
            'Host': 'mp.weixin.qq.com',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36 QBCore/4.0.1301.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2875.116 Safari/537.36 NetType/WIFI MicroMessenger/7.0.5 WindowsWechat',
            'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzI5MTE2NDI2OQ==&scene=124&uin=OTMxMjEwMTIy&key=a97cfd640f4c538a5dd211690fec5bf9ff23db3db375e56754629f2a4100630f3f735200d861602738db6afdf97ec42e38d9ee19f69f034a13d249c4623319077f9f62ed4c43466325f2f575d886e1a7ec080e7434a20cf5a4046828bca9544fda16cc87a940ae8eca57dc31a0acba74c74b9e398900ccd6782098ccba9449d8&devicetype=Windows+10+x64&version=6300002f&lang=zh_CN&a8scene=7&pass_ticket=7sVse3N83I76nZYVGdoQv%2BcT3Y2brTifoLiQm8WTqP0P83%2Bkvp5riUoNNF2N1eg6&fontgear=2',
            'Accept-Language': 'zh-cn',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = (
            ('action', 'getmsg'),
            ('__biz', 'MzI5MTE2NDI2OQ=='),
            ('f', ['json', 'json']),
            ('is_ok', '1'),
            ('scene', '124'),
            ('uin', 'OTMxMjEwMTIy'),
            ('key',
             'a97cfd640f4c538a5dd211690fec5bf9ff23db3db375e56754629f2a4100630f3f735200d861602738db6afdf97ec42e38d9ee19f69f034a13d249c4623319077f9f62ed4c43466325f2f575d886e1a7ec080e7434a20cf5a4046828bca9544fda16cc87a940ae8eca57dc31a0acba74c74b9e398900ccd6782098ccba9449d8'),
            ('pass_ticket', '7sVse3N83I76nZYVGdoQv+cT3Y2brTifoLiQm8WTqP0P83+kvp5riUoNNF2N1eg6'),
            ('wxtoken', ''),
            ('appmsg_token', '1091_Fl2wmkeh5GWVACcKwu7Y_2wFoKcCCYpJFIxL3w~~'),
            ('x5', '0'),
        )

        # 代理ip，失效的话请自行更换，也可以直接去掉
        # proxy = {'https': '114.239.144.61:808'}

        try:
            response = requests.get(
                base_url.format(offset),
                headers=headers,
                params=params,
                cookies=cookies,
                # proxies=proxy
            )
            if 200 == response.status_code:
                all_datas = json.loads(response.text)
                if 0 == all_datas['ret'] and all_datas['msg_count'] > 0:
                    summy_datas = all_datas['general_msg_list']
                    datas = json.loads(summy_datas)['list']
                    for data in datas:
                        try:
                            article_url = data['app_msg_ext_info']['content_url']
                            article_url_list.append(article_url)
                        except Exception as e:
                            continue
        except:
            time.sleep(2)
        time.sleep(1)
    return article_url_list


def get_urls(url):
    try:
        html = requests.get(url, timeout=30).text
    except requests.exceptions.SSLError:
        html = requests.get(url, verify=False, timeout=30).text
    except TimeoutError:
        print('请求超时')
    except Exception:
        print('获取失败')
    src = re.compile(r'data-src="(.*?)"')
    urls = re.findall(src, html)
    if urls is not None:
        url_list = []
        for url in urls:
            url_list.append(url)
        return url_list


def mkdir():
    isExists = os.path.exists(r'E:\表情包')
    if not isExists:
        print('创建目录')
        os.makedirs(r'E:\表情包')  # 创建目录
        os.chdir(r'E:\表情包')  # 切换到创建的文件夹
        return True
    else:
        print('目录已存在，即将保存！')
        return False


def download(filename, url):
    try:
        with open(filename, 'wb+') as f:
            try:
                f.write(requests.get(url, timeout=30).content)
                print('成功下载图片：', filename)
            except requests.exceptions.SSLError:
                f.write(requests.get(url, verify=False, timeout=30).content)
                print('成功下载图片：', filename)
    except FileNotFoundError:
        print('下载失败，非表情包，直接忽略：', filename)
    except TimeoutError:
        print('下载超时：', filename)
    except Exception:
        print('下载失败：', filename)


"""
本项目首发：
B站原创视频：https://www.bilibili.com/video/BV1Vz41187Rt
公众号原创文章：https://mp.weixin.qq.com/s/fVDwNdVDZo_0q6jAMWCGAA
公众号：Python知识圈（id：PythonCircle）
哔哩哔哩：菜鸟程序员的日常
"""

if __name__ == '__main__':
    for url in tqdm(request_data()):
        url_list = get_urls(url)
        mkdir()
        for pic_url in tqdm(url_list):
            try:
                filename = r'E:/表情包/' + pic_url.split('/')[-2] + '.' + pic_url.split('=')[-1]  # 图片的路径
                download(filename, pic_url)
            except:
                continue