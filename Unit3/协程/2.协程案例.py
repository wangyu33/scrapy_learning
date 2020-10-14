#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 2.协程案例.py
# Author: WangYu
# Date  : 2020-09-17

import gevent
from greenlet import greenlet#切换器
import time

def go1():
    while 1:
        print('go1')
        gr2.switch()
        time.sleep(1)

def go2():
    while 1:
        print('go2')
        gr1.switch()
        time.sleep(1)


if __name__ == "__main__":
    gr1 = greenlet(go1)
    gr2 = greenlet(go2)
    gr1.switch()