#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2023/7/7 12:07
# @Author  : Scott Yang
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from PIL import Image


def replace_color(path, org_color, aim_color):
    # 打开图片文件
    image = Image.open(path)

    # 遍历所有像素，将指定颜色替换为新的颜色
    for x in range(image.width):
        for y in range(image.height):
            # 获取当前像素的颜色
            color = image.getpixel((x, y))

            # 如果颜色匹配，将其替换为新的颜色 color exp:(255, 0, 0)
            if color_shake(color, org_color):  # 将红色替换为绿色
                image.putpixel((x, y), aim_color)

    # 保存修改后的图片
    image.save("output.jpg")


def color_shake(color, aim,  shake_range=15):
    for i, v in enumerate(color):
        if not (aim[i] - shake_range < v < aim[i] + shake_range):
            return False

    return True



if __name__ == '__main__':
    # replace_color("org.png", (44, 85, 84), (46,77,110))
    replace_color("org.png", (44, 85, 84), (0,0,255))