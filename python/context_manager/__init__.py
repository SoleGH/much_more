#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2022/6/17 9:34 AM
# @Author  : yangbf
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm


# 方式一，实现__enter__,__exit__
import contextlib


class File(object):
    def __init__(self, file_name, method):
        self.file_obj = open(file_name, method)
    def __enter__(self):
        return self.file_obj
    def __exit__(self, type, value, traceback):
        self.file_obj.close()

with File('demo.txt', 'w') as opened_file:
    opened_file.write('Hola!')


# 方式二 使用contextlib模块装饰器和生成器
@contextlib.contextmanager
def my_open(filename, mode):
    f = open(filename, mode)
    try:
        yield f.readlines()
    except Exception as e:
        print(e)

    finally:
        f.close()

with my_open(r'c:\ip2.txt', 'r') as f:
    for line in f:
        print(line)