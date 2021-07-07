#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : client.py
# Author: WangYu
# Date  : 2020-10-17

from multiprocessing import managers
import multiprocessing
import random, time
import queue

class Queue_Manager(managers.BaseManager):
    pass

if __name__ == '__main__':
    multiprocessing.freeze_support()    #开启分布式支持
    Queue_Manager.register('get_task')
    Queue_Manager.register('get_ans')
    managers = Queue_Manager(address= ('192.168.3.35', 8848), authkey=b'123456')
    managers.connect()
    task, ans = managers.get_task(), managers.get_ans()
    for i in range(1000):
        try:
            data = task.get()
            print('client get ', data)
            ans.put('client ' + str(data+10))
        except:
            pass


