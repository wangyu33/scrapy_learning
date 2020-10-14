#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 3.协程程序开发.py
# Author: WangYu
# Date  : 2020-09-17

import gevent
import greenlet
import time

def wait(name, t):
    for i in range(t):
        print(name, '等待了', i + 1, '秒')
        # time.sleep(1)
        gevent.sleep(1)

# wait('长老',10)
# wait('李磊',10)
# wait('威威',10)


g1 = gevent.spawn(wait, '长老', 10)
g2 = gevent.spawn(wait, '李磊', 10)
g3 = gevent.spawn(wait, '威威', 10)
g1.join()
g2.join()
g3.join()