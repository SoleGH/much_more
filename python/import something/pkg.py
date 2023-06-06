#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/2/1 15:12
# @Author  : Scott Yang
# @Site    :
# @File    : pkg.py
# @Software: PyCharm


# ####### base_pkg未定义 __all__场景 #
from base_pkg import *

print(dir())
# ['ClassBase', 'ConnectTimeout', 'ConnectionError', 'DependencyWarning', 'FileModeWarning', 'HTTPError',
# 'JSONDecodeError', 'NAME', 'NullHandler', 'PreparedRequest', 'ReadTimeout', 'Request', 'RequestException',
# 'RequestsDependencyWarning', 'Response', 'Session', 'Timeout', 'TooManyRedirects', 'URLRequired', '__annotations__',
# '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'adapters',
# 'api', 'auth', 'certs', 'chardet_version', 'charset_normalizer_version', 'check_compatibility', 'codes', 'compat',
# 'cookies', 'delete', 'exceptions', 'fuc_base', 'get', 'head', 'hooks', 'json', 'logging', 'models', 'options',
# 'packages', 'patch', 'post', 'put', 'request', 'session', 'sessions', 'ssl', 'status_codes', 'structures',
# 'urllib3', 'utils', 'warnings']

# ####### base_pkg定义 __all__且仅指定了fuc_base 场景
# from base_pkg import *  # 该语法仅导入指定部分
#
# print(dir())
# # ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__',
# '__spec__', 'fuc_base']
#
# from base_pkg import ClassBase  # 在__all__未指定的情况下依旧可以显式导入其它对象
# print(dir())
# # ['ClassBase', '__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__',
# '__package__', '__spec__', 'fuc_base']

# 直接导入包
# import base_pkg
# print(dir())
# ['__annotations__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'base_pkg']
