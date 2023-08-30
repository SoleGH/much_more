#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/20 14:12
# @Author  : Scott Yang
# @Site    : 
# @File    : nanonets_test.py
# @Software: PyCharm
import json

import requests

import secret

"""
https://app.nanonets.com/#/ocr/test/731945a2-2be1-4ae5-b850-c6698d892f9d?callflow=true
"""

url = 'https://app.nanonets.com/api/v2/OCR/Model/731945a2-2be1-4ae5-b850-c6698d892f9d/LabelFile/?async=false'

# by file
data = {'file': open('./org_table/hm.jpg', 'rb')}
response = requests.post(url, auth=requests.auth.HTTPBasicAuth(secret.NANONETS_SECRET, ''), files=data)

# by url
# headers = {
#     'accept': 'application/x-www-form-urlencoded'
# }
# data = {'urls': ['https://www.eu.lululemon.com/en-lu/content/footer-size-guide2.html']}  # url must be image file
# response = requests.request('POST', url, headers=headers, auth=requests.auth.HTTPBasicAuth(secret.NANONETS_SECRET, ''), data=data)

data = json.loads(response.text)
print(data)
"""
{'message': 'Success', 'result':[]....}
"""
page_index = 0
for page in data["result"]:
    page_index += 1
    table_index = 0
    for table in page["prediction"]:
        table_index += 1
        table_array = []
        for cell in table["cells"]:
            row = cell["row"]
            col = cell["col"]
            value = cell["text"]
            if len(table_array) < row:
                table_array.append([value])
            else:
                table_array[row-1].append(value)

        print(f"****print table, page:{page_index},table:{table_index}*****")
        for row in table_array:
            print(row)


"""
./org_table/adidas_1.jpg
****print table*****
['Product label', '2XS ( 00 )', 'XS ( 0-2 )', 'S ( 4-6 )', 'M ( 8-10 )', 'L ( 12-14 )', 'XL ( 16-18 )', '2XL ( 20 )']
['BUST', '28.5 29.5 "', '30-32 "', '32.5-34.5 "', '35-37 "', '37.5 - 40 "', '40.5 - 43 "', '43.5-46.5 "']
['Waist', '22-23.5 "', '24-26 "', '26.5 28.5 "', '29 - 31 "', '31.5-33.5 "', '34-37 "', '37.5 - 41 "']
['Hip', '31.5 - 33 "', '33.5 - 35.5 "', '36 - 38 "', '38.5 40.5 "', '41 - 43 "', '43.5 - 46 "', '46.5-49 "']
****print table*****
['US', '2XS ( 00 )', 'XS ( 0-2 )', 'S ( 4-6 )', 'M ( 8-10 )', 'L ( 12-14 )', 'XL ( 16-18 )', '2XL ( 20 )']
['UK', '2XS ( 0-2 )', 'XS ( 4-6 )', 'S ( 8-10 )', 'M ( 12-14 )', 'L ( 16-18 )', 'XL ( 20-22 )', '2XL ( 24-26 )']
['DE', '2XS ( 26-28 )', 'XS ( 30-32 ) ===', 'S ( 34-36 )', 'M ( 38-40 )', 'L ( 42-44 )', 'XL ( 46-48 )', '2XL ( 50-52 )']
['FR', '2XS ( 28-30 )', 'XS ( 32-34 )', 'S ( 36-38 )', 'M ( 40-42 )', 'L ( 44-46 )', 'XL ( 48-50 )', '2XL ( 52-54 )']
['IT', '2XS ( 32-34 )', 'XS ( 36-38 )', 'S ( 40-42 )', 'M ( 44-46 )', 'L ( 48-50 )', 'XL ( 52-54 )', '2XL ( 56-58 )']
"""

"""
by url :https://www.adidas.com/us/help/size_charts/women-pants_shorts
error
"""


"""
./org_table/adidas_screenshot.png
****print table*****
['Product label', 'S Tall', 'M Tall', 'L Tall', 'XL Tall', '2XL Tall']
['Waist', '26.5 28.5 "', '29 - 31 "', '31.5 33.5 "', '34 - 37 "', '37.5 - 41 "']
['Hip', '36 - 38 "', '38.5 - 40.5 "', '41 - 43 "', '43.546 "', '46.5 49 "']
['Inseam', '33 "', '33.5 "', '33.5 "', '33.5 "', '34 "']
****print table*****
['Product label', '2XS Petite', 'XS Petite', 'S Petite', 'M Petite', 'L Petite', 'XL Petite', '2XL Petite']
['Waist', '22-23.5 "', '24-26 "', '26.5 - 28.5 "', '29-31 "', '31.5 33.5 "', '34 - 37 "', '37.5 41 "']
['Hip', '31.5 33 "', '33.5 35.5 "', '36 - 38 "', '38.5 40.5 "', '41 - 43 "', '43.5-46 "', '46.5 - 49 "']
['Inseam', '28.5 "', '29 "', '29 "', '29.5 "', '29.5 "', '29.5 "', '30 "']
****print table*****
['Product label', '1X / 14W - 16W', '2X / 18W - 20W', '3X / 22W - 24W', '4X / 26W - 28W']
['Waist', '35 " - 38 1/2 "', '39 " -42 1/2 "', '43 " - 46 1/2 "', '47 " - 50 1/2 "']
['Hip', '43 1/2 " - 47 "', '47 1/2 " - 51 "', '51 1/2 " - 55 "', '55 1/2 " - 59 "']
['Inseam', '31 "', '31 "', '30 1/2 "', '30 "']
****print table*****
['US', '1X ( 14W - 16W )', '2X ( 18W - 20W )', '3X ( 22W - 24W )', '4X ( 26W - 28W )']
['UK', '1X ( 20-22 )', '2X ( 24-26 )', '3X ( 28-30 )', '4X ( 32-34 )']
['DE', '1X ( 46-48 )', '2X ( 50-52 )', '3X ( 54-56 )', '4X ( 58-60 )']
['FR', '1X ( 48-50 )', '2X ( 52-54 )', '3X ( 56-58 )', '4X ( 60-62 )']
['IT', '1X ( 52-54 )', '2X ( 56-58 )', '3X ( 60-62 )', '4X ( 64-66 )']
****print table*****
['Product label', '2XS ( 00 )', 'XS ( 0-2 )', 'S ( 4-6 )', 'M ( 8-10 )', 'L ( 12-14 )', 'XL ( 16-18 )', '2XL ( 20 )']
['Waist ( Pre\nPregnancy )', '22-23.5 "', '24-26 "', '26.5 28.5 "', '29 - 31 "', '31.5-33.5 "', '34 - 37 "', '37.5 41 "']
['Hip', '31.5 - 33 "', '33.5 35.5 "', '36 - 38 "', '38.5 40.5 "', '41-43 "', '43.5 - 46 "', '46.5 49 "']
['Inseam', '30.5 "', '31 "', '31 "', '31.5 "', '31.5 "', '31.5 "', '32 "']
****print table*****
['PRODUCTS', 'SPORTS', 'COLLECTIONS', 'SUPPORT', 'COMPANY INFO', 'FOLLOW']
['Shoes', 'Soccer', 'Back to School', 'Help', 'About Us', 'US']
['Clothing', 'Running', 'adicolor', 'Returns & Exchanges', 'Student Discount', '']
['Accessories', 'Basketball', 'Ultraboost', 'Shipping', 'Military & Healthcare Discount', '']
['Gift Cards', 'Football', 'NMD', 'Order Tracker', 'adidas Stories', '']
['', 'Outdoor', 'Forum', 'Store Locator', 'adidas Apps', '000000']
['New Arrivals', 'Golf', 'Superstar', 'Size Charts', 'Sustainability', '']
['Best Sellers', 'Baseball', 'Running Shoes', 'Gift Card Balance', 'adiClub', 'S']
['Release Dates', 'Tennis', 'adilette', 'How to Clean Shoes', 'Affiliates', '']
['Sale', 'Skateboarding', 'Stan Smith', 'Running Shoe Finder', 'Press', '']
['', 'Training', 'adizero', 'Bra Fit Guide', 'Careers', '']
['', '', 'Tiro', 'Sports Bra Finder', 'California Transparency in Supply Chains Act', '']
['', '', 'EQT', 'Breathing for Running', 'Responsible Disclosure', '']
['', '', '', 'Promotions', 'Transparency in Coverage', '']
['', '', '', '', 'Country Selector', '']
****print table*****
['Product label', '2XS ( 00 )', 'XS ( 0-2 )', 'S ( 4-6 )', 'M ( 8-10 )', 'L ( 12-14 )', 'XL ( 16-18 )', '2XL ( 20 )']
['Waist', '22 - 23.5 "', '24-26 "', '26.5 28.5 "', '29 - 31 "', '31.5 33.5 "', '34 - 37 "', '37.5 - 41 "']
['Hip', '31.5-33 "', '33.5 - 35.5 "', '36 - 38 "', '38.5 40.5 "', '41-43 "', '43.5 - 46 "', '46.5-49 "']
['Inseam', '30.5 "', '31 "', '31 "', '31.5 "', '31.5 "', '31.5 "', '32 "']
****print table*****
['US', '2XS ( 00 )', 'XS ( 0-2 )', 'S ( 4-6 )', 'M ( 8-10 )', 'L ( 12-14 )', 'XL ( 16-18 )', '2XL ( 20 )']
['UK', '2XS ( 0-2 )', 'XS ( 4-6 )', 'S ( 8-10 )', 'M ( 12-14 )', 'L ( 16-18 )', 'XL ( 20-22 )', '2XL ( 24-26 )']
['DE', '2XS ( 26-28 )', 'XS ( 30-32 )', 'S [ 34-36 )', 'M ( 38-40 )', 'L ( 42-44 )', 'XL ( 46-48 )', '2XL ( 50-52 )']
['FR', '2XS ( 28-30 )', 'XS ( 32-34 )', 'S [ 36-38 )', 'M ( 40-42 )', 'L ( 44-46 )', 'XL ( 48-50 )', '2XL ( 52-54 )']
['IT', '2XS ( 32-34 )', 'XS ( 36-38 )', 'S ( 40-42 )', 'M ( 44-46 )', 'L ( 48-50 )', 'XL ( 52-54 )', '2XL ( 56-58 )']
"""