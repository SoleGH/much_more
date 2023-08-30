#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/20 12:14
# @Author  : Scott Yang
# @Site    : 
# @File    : img2table_test.py
# @Software: PyCharm


# pip install img2table
from img2table.document import Image
from img2table.ocr import TesseractOCR

# Instantiation of the image
img = Image(src="./org_table/adidas_1_tb_1.jpg")

# Instantiation of the OCR, Tesseract, which requires prior installation
ocr = TesseractOCR(lang="eng")

# Table identification and extraction
pdf_tables = img.extract_tables(ocr=ocr)

# We can also create an excel file with the tables
img.to_xlsx('tables.xlsx', ocr=ocr)
"""
*******************
仅识别到一行数据，且数据混在一个单元格
*********************
"""
