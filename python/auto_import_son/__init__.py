#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/6 14:57
# @Author  : Scott Yang
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
import os
import glob

dir_path = os.path.dirname(os.path.realpath(__file__))

files = glob.glob(os.path.join(dir_path, "*.py"))

for file in files:
    if file != os.path.realpath(__file__):
        module_name = os.path.splitext(os.path.basename(file))[0]
        exec(f"from .{module_name} import *")