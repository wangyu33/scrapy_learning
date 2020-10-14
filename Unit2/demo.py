# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # File  : demo.py
# # Author: WangYu
# # Date  : 2020-08-28
#
# import requests
# from pprint import pprint
# from bs4 import BeautifulSoup
#
# url = 'http://www.baidu.com'
# response = requests.get(url).content
#
# soup = BeautifulSoup(response, 'lxml')
# # pprint(soup.head())
# #
# # pprint(soup)
# # pprint(soup.head.attrs)
# pprint(soup.find('p'))
# pprint(soup.find_all('p'))
# pprint(soup.find_all('p')[1])

from lxml import etree
import requests
import pandas as pd


def get_dt():
    dt = []
    for i in range(1, 10):
        url = 'http://www.planning.org.cn/news/newslist?cid=12&page={}.format(str(i))'
        html = requests.get(url).text
        txt = etree.HTML(html)
        txt2 = txt.xpath('//div[@class="fl w680 overh xh_list_boxb"]/div')
        for t in txt2[1:]:
            row = []
            title = t.xpath('h4/a/text()')[0]
            url = t.xpath('h4/a/@href')[0]
            row.append(title)
            row.append('http://www.planning.org.cn' + url)
            dt.append(row)
    return dt


pd.DataFrame(get_dt(), columns=['title', 'url']).to_excel('C:/Users/XXX/test/planning.xlsx')  # 导出为excel
