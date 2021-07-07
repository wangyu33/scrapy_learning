#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : Sever.py
# Author: WangYu
# Date  : 2020-10-17

from multiprocessing import managers
import multiprocessing
import random, time
import queue

task_queue = queue.Queue()
ans_queue = queue.Queue()


def return_task():
    return task_queue


def return_ans():
    return ans_queue


class Queue_Manager(managers.BaseManager):
    pass


if __name__ == '__main__':
    multiprocessing.freeze_support()  # 开启分布式支持
    Queue_Manager.register('get_task', callable=return_task)
    Queue_Manager.register('get_ans', callable=return_ans)
    managers = Queue_Manager(address=('192.168.3.35', 8848), authkey=b'123456')
    managers.start()
    task, ans = managers.get_task(), managers.get_ans()
    for i in range(1000):
        print('add data ', i)
        task.put(i)
    print("waitting for------")
    for i in range(1000):
        res = ans.get()
        print('get data', res)

    managers.shutdown()
