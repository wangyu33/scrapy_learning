#!/usr/bin/env python
# -*- coding: utf-8 -*-
# File  : re_demo.py
# Author: WangYu
# Date  : 2020-10-14

import re

content = """Xiaoshuaib has 100 bananas;
Xiaoshuaib has 100 bananas;
Xiaoshuaib has 100 bananas;
Xiaoshuaib has 100 bananas;"""
res = re.findall('Xi.*?(\d+)\s.*?s;',content,re.S)
print(res)