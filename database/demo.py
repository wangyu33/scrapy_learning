#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : demo.py
# Author: WangYu
# Date  : 2020/12/2

import MySQLdb
import pymysql
import pandas as pd
from sqlalchemy import create_engine

host = '127.0.0.1'
port = 3306
db = 'test'
user = 'root'
password = 'aptx4869'

engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s") % (user, password, host, db))

try:
    df = pd.DataFrame([[1,'x'],[2,'y']],columns=list('ab'))
    df.to_sql('test1',con=engine,if_exists='replace',index=False)
except Exception as e:
    print(e)
