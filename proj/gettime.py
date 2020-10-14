#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : gettime.py
# Author: WangYu
# Date  : 2020-08-25


import time, datetime


def gettime():
    for x in range(24):
        a = datetime.datetime.now().strftime("%Y-%m-%d") + " %2d:00:00" % x

        timeArray = time.strptime(a, "%Y-%m-%d %H:%M:%S")

        timeStamp = int(time.mktime(timeArray))
        print(timeStamp)


if __name__ == "__main__":
    gettime()