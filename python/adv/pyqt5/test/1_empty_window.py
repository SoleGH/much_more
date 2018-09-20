#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

In this example, we create a simple
window in PyQt5.

author: Jan Bodnar
website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget


if __name__ == '__main__':

    app = QApplication(sys.argv)  # 创建应用对象

    w = QWidget()  # 构造创口windows
    w.resize(250, 150)  # 设置窗口大小，（宽，高）
    w.move(300, 300)  # 设置窗口位置，屏幕左上角为（0,0）
    w.setWindowTitle('Simple')  # 标题栏标题名称
    w.show()  # 在内存中构建窗口，并显示，

    sys.exit(app.exec_())  # 监听关闭事件
