#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/19 10:10
# @Author  : Scott Yang
# @Site    : 
# @File    : tesseract.py
# @Software: PyCharm
"""
pip install pytesseract
"""

import pytesseract
import cv2

# 读取图片
img = cv2.imread('adidas_1.jpg')

# 将图片转为灰度图像
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 对图像进行二值化处理
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# 使用OCR进行识别
text = pytesseract.image_to_string(thresh, lang='eng', config='--psm 6')

# 打印输出结果
print(text)