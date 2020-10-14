#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : demo2.py
# Author: WangYu
# Date  : 2020-10-13

from threading import Thread
import time


def counter():
    i = 0
    for _ in range(50000000):
        i = i + 1

    return True


def main():
    l = []
    start_time = time.time()

    for i in range(2):
        t = Thread(target=counter)
        t.start()
        l.append(t)
        t.join()    #串行快一些我

    # for t in l:
    #     t.join()  #并行慢一些

    end_time = time.time()
    print("Total time: {}".format(end_time - start_time))


if __name__ == '__main__':
    main()