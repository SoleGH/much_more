#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/19 10:00
# @Author  : Scott Yang
# @Site    : 
# @File    : camlot_test.py
# @Software: PyCharm
import camelot

# 将图像转换为PDF（例如使用img2pdf库）
# ...

tables = camelot.read_pdf('adidas_1.pdf')
for table in tables:
    print(table.df)  # 打印DataFrame格式的表格

# 仅支持将文本形式的PDF转化为表格