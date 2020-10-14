#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : 1.协程.py
# Author: WangYu
# Date  : 2020-09-17

def go():
    print(1)
    # yield 相当于带断点的return
    yield 1
    print(11)
    yield 11
    print(111)
    yield 111


# 实现函数分段执行
my = go()
print(type(my))
print(next(my))
print(next(my))
