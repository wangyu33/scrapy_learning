#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 2.多进程pid.py
# Author: WangYu
# Date  : 2020-10-14

import multiprocessing
import time
def run(name):
    time.sleep(2)
    print(name, " 进程启动")

if __name__ == '__main__':
    mp = multiprocessing.Process(target=run, args=("LJ",))
    mp.start()
    mp.join() # 等待进程执行完毕