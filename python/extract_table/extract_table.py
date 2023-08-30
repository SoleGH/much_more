#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/6/19 17:00
# @Author  : Scott Yang
# @Site    : 
# @File    : extract_table.py
# @Software: PyCharm

"""
https://extracttable.com/resources/tutorial.html
"""
import os
import time
from io import BytesIO

from ExtractTable import ExtractTable
from PIL import Image

import secret

print(ExtractTable.VERSION)  # ExtractTable_2.4.0

api_key = secret.EXTRACT_TABLE_API_KEY
et_sess = ExtractTable(api_key)


def extract_table(path):
    global et_sess
    # use file path
    # table_data = et_sess.process_file(filepath=path, output_format="df")

    # use image object
    img = Image.open(path)
    filepath = f'./{int(time.time() * 1000)}.png'
    img.save(filepath, format='PNG')
    table_data = et_sess.process_file(filepath=filepath, output_format="df")
    print(table_data)

    # for df in table_data:
    #     data_list = list(df.values.tolist())
    #     for i in data_list:
    #         print(i)
    # os.remove(filepath)
    print(list(table_data[0].values.tolist()))
    usage = et_sess.check_usage()
    print(usage)


if __name__ == '__main__':
    # extract_table('./org_table/adidas_1.jpg')
    """
    {'credits': 10, 'queued': 0, 'used': 4}
    [               0           1           2  ...           5           6           7
    0  Product label    2XS (00)    XS (0-2)  ...   L (12-14)  XL (16-18)    2XL (20)
    1           BUST  28.5 29.5"      30 32"  ...    37.5 40"    40.5 43"  43.5 46.5"
    2          Waist    22 23.5'      24 26"  ...  31.5 33.5"      34 37"    37.5 41"
    3            Hip    31.5 33"  33.5 35.5"  ...      41 43"    43.5 46"    46.5 49"
    
    [4 rows x 8 columns],     0            1           2  ...          5           6            7
    0  US     2XS (00)    XS (0-2)  ...  L (12-14)  XL (16-18)     2XL (20)
    1  UK    2XS (0-2)    XS [4-6]  ...  L (16-18)  XL (20-22)  2XL (24-26)
    2  DE  2XS (26-28)  XS (30-32)  ...  L (42-44)  XL [46-48]  2XL (50-52)
    3  FR  2XS (28-30)  XS [32-34]  ...  L (44-46)  XL (48-50)  2XL (52-54)
    4  IT  2XS (32-34)  XS (36-38)  ...  L (48-50)  XL (52-54)  2XL (56-58)
    
    [5 rows x 8 columns]]
    
    ['Product label', '2XS (00)', 'XS (0-2)', 'S (4-6)', 'M (8-10)', 'L (12-14)', 'XL (16-18)', '2XL (20)']
    ['BUST', '28.5 29.5"', '30 32"', '32.5 34.5"', '35 37"', '37.5 40"', '40.5 43"', '43.5 46.5"']
    ['Waist', "22 23.5'", '24 26"', '26.5 28.5"', '29 31"', '31.5 33.5"', '34 37"', '37.5 41"']
    ['Hip', '31.5 33"', '33.5 35.5"', '36 38"', '38.5 40.5', '41 43"', '43.5 46"', '46.5 49"']
    
    ['US', '2XS (00)', 'XS (0-2)', 'S (4-6)', 'M (8-10)', 'L (12-14)', 'XL (16-18)', '2XL (20)']
    ['UK', '2XS (0-2)', 'XS [4-6]', 'S (8-10)', 'M (12-14)', 'L (16-18)', 'XL (20-22)', '2XL (24-26)']
    ['DE', '2XS (26-28)', 'XS (30-32)', 'S (34-36)', 'M (38-40)', 'L (42-44)', 'XL [46-48]', '2XL (50-52)']
    ['FR', '2XS (28-30)', 'XS [32-34]', 'S (36-38)', 'M (40-42)', 'L (44-46)', 'XL (48-50)', '2XL (52-54)']
    ['IT', '2XS (32-34)', 'XS (36-38)', 'S (40-42)', 'M (44-46)', 'L (48-50)', 'XL (52-54)', '2XL (56-58)']
    """

    # extract_table('./org_table/adidas_1_tb_1.jpg')
    """
    [               0           1           2  ...           5           6           7
    0  Product label    2XS (00)    XS (0-2)  ...   L (12-14)  XL (16-18)    2XL (20)
    1           BUST  28.5 29.5"      30 32"  ...    37.5 40"    40.5 43"  43.5 46.5"
    2          Waist    22 23.5"      24 26"  ...  31.5 33.5"      34 37"    37.5 41"
    3            Hip    31.5 33"  33.5 35.5"  ...      41 43"    43.5 46"    46.5 49"
    
    [4 rows x 8 columns]]
    ['Product label', '2XS (00)', 'XS (0-2)', 'S (4-6)', 'M (8-10)', 'L (12-14)', 'XL (16-18)', '2XL (20)']
    ['BUST', '28.5 29.5"', '30 32"', '32.5 34.5"', '35 37"', '37.5 40"', '40.5 43"', '43.5 46.5"']
    ['Waist', '22 23.5"', '24 26"', '26.5 28.5"', '29 31"', '31.5 33.5"', '34 37"', '37.5 41"']
    ['Hip', '31.5 33"', '33.5 35.5"', '36 38"', '38.5 40.5"', '41 43"', '43.5 46"', '46.5 49"']
    {'credits': 10, 'queued': 0, 'used': 6}
    """

    extract_table('./org_table/adidas_2_tb_1.jpg')
    """
    [               0             1           2           3         4         5
    0  Product label        S Tall      M Tall      L Tall   XL Tall  2XL Tall
    1          Waist  26.5 - 28.5"      29 31"  31.5 33.5"    34 37"  37.5 41"
    2            Hip        36 38"  38.5 40.5"      41 43"  43.5 46"  46.5 49"
    3         Inseam           33"       33.5"       33.5"     33.5"       34"]
    ['Product label', 'S Tall', 'M Tall', 'L Tall', 'XL Tall', '2XL Tall']
    ['Waist', '26.5 - 28.5"', '29 31"', '31.5 33.5"', '34 37"', '37.5 41"']
    ['Hip', '36 38"', '38.5 40.5"', '41 43"', '43.5 46"', '46.5 49"']
    ['Inseam', '33"', '33.5"', '33.5"', '33.5"', '34"']
    {'credits': 10, 'queued': 0, 'used': 7}
    """

    # extract_table('./org_table/adidas_screenshot.png')
    """
    ['Product Labe', '2XS (00)', 'XS 10-21', '5(4-6)', 'M (5-10)', 'L 112-143', 'XL (16-18)', 'ZXL (20)']
    ['Waist', '22 23.5', '24-26', '26.5.20.5', '29.31', '31.5-33.57', '34-37"', '37.5-41']
    ['Hip', '31.5.33', '33.5-35.57', '36-38"', '38.5.40.5', '41.43', '43.5-46', '465-49']
    ['', '30.5"', '31', '31"', '31.5"', '31.3"', '31.5', '32"']
    
    ['us', '2XS (00)', 'XS 10-21', 'S(4-6)', 'M (8-10)', 'L 112-143', 'XL (16-18)', '2XL 1203']
    ['', '', '', '', '', '', '', '2XL(24-26)']
    ['', '', '', 'S134-344', '', '', '', '2XL(50-52)']
    ['', '', '', '', '', '', 'XL(48-50)', '2XL 02-54']
    ['', '', '', '$ 140,421', '', 'L(48-50)', '', '2XL(54-58)']
    ['Product Label', 'S Tall', 'M Tall', 'L Tall', 'XL Tall', '2XL Tall']
    ['Waist', '26.5-28.5', '29-31*', '31.5-33.5"', '34-37"', '37.5-41']
    ['Hig', '', '', '41-43', '43.5-46', '46.5-49']
    ['inseam', '', '33.5"', '33.5', '33.5°', '34']
    ['Product La', '2XS Petite', 'XS Pecite', 'S Petite', 'M Petite', 'L Petite', 'XL Patite', '2XL Pecite']
    ['Waist', '22 23.5', '24-26', '26.5-20.5', '29-31"', '31.5-335', '34-37', '37.5-41']
    ['Hip', '', '35.5"', '', '38.5-40.51', '41-43', '43.5-46', '46.5-49']
    ['Inseam', '28.5', '', '29"', '29.5*', '29.5', '29.5"', '30"']
    ['Product tabel', '1X/16W-16W', '2X/18W 20W', '3X/22W-24W', '4X/26W-28W']
    ['Waist', '-38 1/2"', '39 - 42 1/2"', '43° - 46 1/2"', '47" - 50 1/2"']
    ['', "$3.1/2 47'", '47172-51"', '51 172 - 55"', '55 1/2 - 59']
    ['', '', '', '30 1/2', "30'"]
    ['US', '1XI14W-16WT', '2X(18W-20W)', '3X (22W - 24W)', '4x 126W - 28W1']
    ['UK', '1x (20-22)', '2X124-241', '3X(28-30)', '4X (32-36)']
    ['', 'IX 146-481', '2X150-52|', '3X (54-56', '4X(58-60)']
    ['', '', '2X152-54]', '3X(54-58)', '4X160-673']
    ['', '', '2X156-501', '', '4X 664-663']
    ['Product lat', '2XS (00)', 'XS 10-21', 'S(6-61', 'M(8-10)', 'L 112-14)', 'XL(16-18)', '2XL (20)']
    ['Waist (Pre- Pregnancy', '22-735', '24-26', '265-28.5', '29.31"', '31.5-3357', '34-37', '37.5-41*']
    ['Hip', '31.5 33', '335-35.5"', '36-387', '38.5-40.57', '41-43', '43.5-46', '465-49"']
    ['Inseam', "30.5'", '', '31 31', "31.5'", '31.57', '31.5"', '32"']
    ['PRODUCTS', 'SPORTS', 'COLLECTIONS', 'SUPPORT', 'COMPANY INFO', 'FOLLOW']
    ['', '', '', '', '', 'US']
    ['', '', '', '', '', 'o']
    ['', '', '', '', 'adiClub', '']
    ['', '', '', '', 'Affiliates Affiliates', '']
    ['', 'Training', '', 'Bra Fit Guide', 'Careers', '']
    ['', '', '', 'ports Bro Finder', 'Chains Act', '']
    ['', '', '', 'Running', 'Responsible Disclosure', '']
    ['', '', '', '', 'Transparen Coverage', '']
    ['', '', '', '', 'Country Selector', '']
    {'credits': 10, 'queued': 0, 'used': 8}
    """
