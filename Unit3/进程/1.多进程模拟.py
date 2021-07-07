#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 1.多进程模拟.py
# Author: WangYu
# Date  : 2020-10-14

import multiprocessing
import os
def go(N, name,queue):
    print('子进程运行中，pid=%d...' % os.getpid())  # os.getpid获取当前进程的进程号
    print('子进程将要结束...')
    for i in range(N):
        queue.put(str(i) + name)


if __name__ == '__main__':
    queue = multiprocessing.Manager().Queue()
    processlist = []
    name = ['a','b','c','d','e']
    for i in name:
        process = multiprocessing.Process(target=go, args=(50, i, queue))
        process.start()
        processlist.append(process)
    print('start')
    for p in processlist:
        p.join()
    while not queue.empty():
        data = queue.get()
        print(data)