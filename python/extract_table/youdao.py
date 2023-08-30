#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/20 10:52
# @Author  : Scott Yang
# @Site    : 
# @File    : youdao.py
# @Software: PyCharm
# https://ai.youdao.com/DOCSIRMA/html/ocr/api/bgocr/index.html
# -*- coding: utf-8 -*-
# import sys
import json
import uuid
# from imp import reload

import requests
import base64
import hashlib
import time

import secret

# reload(sys)
# sys.setdefaultencoding('utf-8')

YOUDAO_URL = 'https://openapi.youdao.com/ocr_table'
APP_KEY = secret.YOUDAO_APP_ID
APP_SECRET = secret.YOUDAO_SECRET


def truncate(q):
    if q is None:
        return None
    q_utf8 = q.decode("utf-8")
    size = len(q_utf8)
    return q_utf8 if size <= 20 else q_utf8[0:10] + str(size) + q_utf8[size - 10:size]


def encrypt(signStr):
    hash_algorithm = hashlib.sha256()
    hash_algorithm.update(signStr.encode('utf-8'))
    return hash_algorithm.hexdigest()


def do_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    return requests.post(YOUDAO_URL, data=data, headers=headers)


def connect(path):
    f = open(path, 'rb')  # 二进制方式打开图文件
    q = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
    f.close()

    data = {}
    data['type'] = '1'
    data['q'] = q
    data['docType'] = 'json'
    data['signType'] = 'v3'
    curtime = str(int(time.time()))
    data['curtime'] = curtime
    salt = str(uuid.uuid1())
    signStr = APP_KEY + truncate(q) + salt + curtime + APP_SECRET
    sign = encrypt(signStr)
    data['appKey'] = APP_KEY
    data['salt'] = salt
    data['sign'] = sign

    response = do_request(data)
    print(json.loads(response.content.decode('utf-8')))


if __name__ == '__main__':
    # connect('./org_table/adidas_1.jpg')  # 识别到了表格外的内容，而且部分括号识别错误
    connect('./org_table/adidas_1_tb_1.jpg')