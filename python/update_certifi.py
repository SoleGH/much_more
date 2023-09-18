#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/9/5 09:54
# @Author  : Scott Yang
# @Site    : 
# @File    : update_certifi.py
# @Software: PyCharm
import requests
import certifi


# 获取最新的根证书列表
updated_cert_data = requests.get("https://curl.se/ca/cacert.pem").text

# 将最新的根证书数据写入 certifi 的证书文件
with open(certifi.where(), "w") as cert_file:
    cert_file.write(updated_cert_data)

print("Root certificates updated successfully.")