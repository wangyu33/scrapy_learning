#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : demo.py
# Author: WangYu
# Date  : 2020-10-23


import pandas as pd
import tushare as ts
import requests
import json
import functools
import random
import time
import tqdm
import numpy as np
# import talib as ta
import tqsdk.tafunc as tafunc
import tqsdk.ta as ta
import multiprocessing
import mpl_finance
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib.pylab import date2num
import matplotlib as mpl
from requests.adapters import HTTPAdapter
import urllib3
import MySQLdb
import pymysql
from sqlalchemy import create_engine
from datetime import datetime
import re

host = '127.0.0.1'
port = 3306
db_name = 'test'
user = 'root'
password = 'aptx4869'
engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s") % (user, password, host, db_name))
db = pymysql.connect(host='localhost',port=3306,user='root',passwd='aptx4869',
                   db=db_name,charset='utf8')
cur=db.cursor()

urllib3.disable_warnings()

def set_user_agent():
    USER_AGENTS = [
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5"
    ]
    user_agent = random.choice(USER_AGENTS)
    return user_agent

def cmp(a, b):
    if a[1] < b[1]:
        return 1
    elif a[1] > b[1]:
        return -1
    else:
        return 0

def sql2df(name_cur,name_tab_str):
    #获取表内数据
    sql_data='''select * from %s; '''%name_tab_str
    name_cur.execute(sql_data)
    data=name_cur.fetchall()
    #获取列名
    cols=[i[0] for i in name_cur.description]
    #sql内表转换pandas的DF
    df=pd.DataFrame(np.array(data),columns=cols)
    df[['open','high','low','close', 'volume', 'download_data']] = df[['open','high','low','close', 'volume', 'download_data']].apply(pd.to_numeric)
    return df

def table_exists(con,table_name):        #这个函数用来判断表是否存在
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1        #存在返回1
    else:
        return 0

def get_sys_data():
    dt = datetime.now()
    data = str(dt.year) + (str(dt.month) if len(str(dt.month)) > 1 else ('0' + str(dt.month))) +  (str(dt.day) if len(str(dt.day)) > 1 else ('0' + str(dt.day)))
    return data

class dragon(object):
    def __init__(self):
        self.stock = self.getStock()
        self.headers = {'User-Agent': set_user_agent(),
                        'Connection': 'close'}

    # def refresh_mysql(self):
    #     ts.set_token('00057629d002692bb383694686c77acea2c10a57f8c224201db155f5')
    #     pro = ts.pro_api()
    #     data = pro.stock_basic()
    #     # # 排除上市不满2年的
    #     data = data[data.list_date.values.astype(np.int32) <= 20191101]
    #     # # 排除ST股票
    #     data = data[~ data.name.str.contains("ST")]
    #     data = data.sort_values(by='industry')
    #     data.to_csv("stocks.csv")
    #     code = []
    #     for i in data.ts_code:
    #         code.append(i[-2:] + i[:6])
    #     data.ts_code = code
    #     #加载入
    #     print('下载数据到数据库')
    #     engine = create_engine(str(r"mysql+mysqldb://%s:" + '%s' + "@%s/%s") % (user, password, host, db))
    #     scale = 240
    #     for code_temp in tqdm.tqdm(code):
    #         df = self.getdata_day(code_temp, scale=scale)
    #         df.to_sql('test1', con=engine, if_exists='replace', index=False)




    def getStock(self):
        # data = ts.get_stock_basics()
        ts.set_token('00057629d002692bb383694686c77acea2c10a57f8c224201db155f5')
        pro = ts.pro_api()
        data = pro.stock_basic()
        # 排除亏损的股票
        # data = data[data.npr > 0.0]
        # # 排除上市不满2年的
        # data = data[data.timeToMarket <= 20190801]
        data = data[data.list_date.values.astype(np.int32) <= 20191101]
        # data = data[data.pe <= 200]
        # # 排除ST股票
        data = data[~ data.name.str.contains("ST")]
        # # print(data)
        data = data.sort_values(by='industry')
        data.to_csv("stocks.csv")
        # # print(set(data.industry))
        code = []
        for i in data.ts_code:
            code.append(str.lower(i[-2:]) + i[:6])
        # data = pd.read_csv('../因子选股/stocks.csv')
        # code = []
        # for i in data.iterrows():
        #     temp = i[1]
        #     code_temp = '0' * (6-len(str(temp[0]))) + str(temp[0])
        #     code.append(code_temp)
        # data['code'] = code
        return code

    def getdata_day(self, id, scale = 240, datalen = 280):
            # 日线：scale = 240  小时：scale：60
            # table_name = id + '_' + str(scale) + '_' +str(datalen)
            # if table_exists(cur, table_name):
            #     data = sql2df(cur, table_name)
            #     if str(data['download_data'].values[0]) == get_sys_data():
            #         return data

            url = 'https://quotes.sina.cn/cn/api/json_v2.php/CN_MarketDataService.getKLineData?symbol=' \
                     + str(id) + '&scale=' + str(scale) + '&datalen=' + str(datalen)
            requests.adapters.DEFAULT_RETRIES = 3
            # requests.packages.urllib3.disable_warnings()
            s = requests.session()
            s.keep_alive = False
            try:
                req = requests.get(url, headers=self.headers, timeout=30,verify=False)
            except:
                print('Max retries exceeded with url')
                return []
            rsp = req.content.decode()
            res_json = json.loads(rsp)
            # 关闭响应包
            req.close()

            bar_list = []
            if not res_json:
                return []
            # res_json.reverse()

            for line in res_json:
                bar = {}
                bar['datetime'] = line['day']
                bar['open'] = float(line['open'])
                bar['high'] = float(line['high'])
                bar['low'] = float(line['low'])
                bar['close'] = float(line['close'])
                bar['volume'] = int(line['volume'])
                bar['download_data'] = get_sys_data()
                bar_list.append(bar)

            df = pd.DataFrame(data=bar_list)
            # df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            return df

    def MA(self, arr ,len):
        # return sum(arr[-len:])/len
        temp = arr[-len:]
        return sum(arr[-len:]) / len

    def candle_plot(self, code):
        def format_date(x, pos):
            if x < 0 or x > len(date_tickers) - 1:
                return ''
            return date_tickers[int(x)]

        df = self.getdata_day(code, 240, 260)
        df['5'] = df.close.rolling(5).mean()
        df['20'] = df.close.rolling(20).mean()
        df['30'] = df.close.rolling(30).mean()
        df['60'] = df.close.rolling(60).mean()
        df['120'] = df.close.rolling(120).mean()
        # df['250'] = df.close.rolling(250).mean()
        date_tickers = df['datetime'].copy().values
        df['datetime'] = pd.to_datetime(df['datetime']).map(date2num)
        df['dates'] = np.arange(0, len(df))

        # date_tickers = df.trade_date2.values
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
        # 绘制K线图
        mpl_finance.candlestick_ochl(
            ax=ax,
            quotes=df[['dates', 'open', 'close', 'high', 'low']].values,
            width=0.7,
            colorup='r',
            colordown='g',
            alpha=0.7)
        # 绘制均线
        for ma in ['5', '20', '30', '60', '120']:
            plt.plot(df['dates'], df[ma])
        plt.legend()
        ax.set_title(code, fontsize=20)
        plt.show()




    def ZJFZ_kdj(self, time_system = 'day'):
        '''
        ZJFZ

        VAR2:=REF(LOW,1);
        VAR3:=SMA(ABS(LOW-VAR2),3,1)/SMA(MAX(LOW-VAR2,0),3,1)*100;
        VAR4:=EMA(VAR3*10,3);
        VAR5:=LLV(LOW,13);
        VAR6:=HHV(VAR4,13);
        VAR7:=EMA(IF(LOW<=VAR5,(VAR4+VAR6*2)/2,0),3)/618;
        VAR8:=IF(VAR7>500,500,VAR7);
        STICKLINE(VAR8>-120,0,VAR8,3,1),COLORGRAY;
        STICKLINE(VAR8>1 AND "KDJ.J">REF("KDJ.J",1) AND REF("KDJ.J",1)<REF("KDJ.J",2),0,VAR8,3,0),COLORRED;
        STICKLINE(VAR8>0.1 AND VAR8<1 AND "KDJ.J">REF("KDJ.J",1) AND REF("KDJ.J",1)<REF("KDJ.J",2),0,VAR8,3,0),COLOR00FFFF;
        '''
        time1 = time.time()
        ans = []
        if time_system == 'day':
            day = 240
        elif time_system == 'week':
            day = 1200
        for code in tqdm.tqdm(self.stock):
            count = 0
            if code[0] == '3':
                continue
            data = self.getdata_day(code, 1200, 260)
            if len(data) < 60:
                continue
            if data['close'][0] < 6:
                continue
            var2 = tafunc.ref(data['low'], 1)
            var3 = tafunc.sma(tafunc.abs(data['low']-var2), 3, 1) / tafunc.sma(tafunc.max(data['low'], var2), 3, 1) * 100
            var4 = tafunc.ema(var3 * 10, 3)
            var5 = tafunc.llv(data['low'], 13)
            var6 = tafunc.hhv(var4, 13)
            for i in range(len(data['low'])):
                a = data['low'][i]
                b = var5[i]
                if not np.isnan(b) and a <= b:
                    var4[i] =  (var4[i] + var6[i]*2)/2
                else:
                    var4[i] = 0

            var7 = tafunc.ema(var4, 3) / 618
            kdj = ta.KDJ(data, 9, 3, 3)
            j = kdj['j']
            gold = tafunc.crossup(kdj['k'], kdj['d'])
            j1 = tafunc.ref(j, 1)
            for i in range(len(j)):
                if np.isnan(j1[i]):
                    var7[i] = 0
                    continue
                # if all((var7[i] > 0.01 , gold[i] > 0)) or all((var7[i] > 0.01 , j[i] > j1[i])):
                if all((var7[i] > 0.01 , gold[i] > 0)):
                    var7[i] = 1
                else:
                    var7[i] = 0

            if np.sum(var7[-4:]) > 0:
                # print(code)
                ans.append(code)
        with open('ZJFZ_kdj.txt', "w") as f:
            for c in ans:
                f.write(c + '\n')
        time2 = time.time()
        print('ZJFZ_kdj' + '运行时间：', time2 - time1)
        return ans




    def macd_double(self):
        time1 = time.time()
        #
        # data = self.getdata_day('000001', 240, 260)
        # close = data['close']
        # kdj = ta.KDJ(data, 9, 3, 3)
        # gold = tafunc.crossup(kdj['k'], kdj['d'])
        ans = []
        for code in tqdm.tqdm(self.stock):
            count = 0
            if code[0] == '3':
                continue
            data = self.getdata_day(code, 240, 260)
            data30 = self.getdata_day(code, 60, 65)
            if len(data) < 60:
                continue
            if data['close'][0] < 6:
                continue
            macd240 = ta.MACD(data, 12, 26, 9)
            macd30 = ta.MACD(data30, 12, 26, 9)
            gold240 = tafunc.crossup(macd240['diff'], macd240['dea'])
            gold30 = tafunc.crossup(macd30['diff'], macd30['dea'])
            if np.sum(gold240[-3:].values) > 0 and np.sum(gold30[-5:].values) > 0:
                print('\n'+ code)
                ans.append(code)

            with open('double_macd.txt', "w") as f:
                for c in ans:
                    f.write(c[0] + '\n')
        time2 = time.time()
        print('double_macd' + '运行时间：', time2 - time1)




    def dragon_MA_dense(self, time_system = 'day'):
        dragon_week_code = []
        time1 = time.time()

        for code in tqdm.tqdm(self.stock):
            count = 0
            if code[0] == '3':
                continue
            if time_system == 'day':
                data = self.getdata_day(code, 240, 260)
            elif time_system == 'week':
                data = self.getdata_day(code, 1200, 65)
            elif time_system == 'h30':
                data = self.getdata_day(code, 30, 65)
            if len(data) < 60:
                continue
            if data['close'][0] < 6:
                continue
            ma5 = self.MA(data['close'], 5)
            ma10 = self.MA(data['close'], 10)
            ma20 = self.MA(data['close'], 20)
            ma30 = self.MA(data['close'], 30)
            ma45 = self.MA(data['close'], 45)
            ma60 = self.MA(data['close'], 60)
            if time_system == 'day':
                ma120 = self.MA(data['close'], 120)
                ma250 = self.MA(data['close'], 250)
                ma = [ma5, ma10, ma20, ma30, ma45, ma60, ma120, ma250]
            else:
                ma = [ma5, ma10, ma20, ma30, ma45, ma60]
            h = data['high'].values[-1]
            l = data['low'].values[-1]
            h = h + h * 0.02
            l = l - l * 0.02
            for k in ma:
                if k > l  and k < h:
                    count += 1
            dragon_week_code.append((code, count))
            # print(code, count)
        dragon_week_code = sorted(dragon_week_code, key=functools.cmp_to_key(cmp))
        filename = time_system + '.txt'
        with open(filename, "w") as f:
            for c in dragon_week_code[:150]:
                f.write(c[0] + '\n')
        time2 = time.time()
        print(filename + '运行时间：', time2 - time1)
        return [c[0] for c in dragon_week_code[:150]]



if __name__ == '__main__':
    a = dragon()
    zjfz = a.ZJFZ_kdj()
    ma240 = a.dragon_MA_dense('day')
    # a.dragon_MA_dense('h30')
    a.dragon_MA_dense('week')
