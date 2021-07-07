#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : demo2.py
# Author: WangYu
# Date  : 2020/12/2

import numpy as np
import pandas as pd
import pymysql
import re
#python连接数据库test50，建立游标
db=pymysql.connect(host='localhost',port=3306,user='root',passwd='aptx4869',
                   db='test',charset='utf8')
cur=db.cursor()
#获取数据库中表列名，顺序维持不乱

def sql2df(name_cur,name_tab_str):
    #获取表内数据
    sql_data='''select * from %s; '''%name_tab_str
    name_cur.execute(sql_data)
    data=name_cur.fetchall()
    #获取列名
    cols=[i[0] for i in name_cur.description]
    #sql内表转换pandas的DF
    df=pd.DataFrame(np.array(data),columns=cols)
    return df


def table_exists(con,table_name):        #这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = str([con.fetchall()])
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1        #存在返回1
    else:
        return 0

table_exists(cur, 'test1')
df_student=sql2df(cur,'test1')

