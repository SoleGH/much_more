#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows an icon
in the titlebar of the window.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon


# 封装窗口创建
class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setGeometry(300, 300, 300, 220)  # resize,move 合体，参数分别代表屏幕坐标的x、y和窗口大小的宽、高
        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('../resources/mini_icon.png'))  # 创建icon对象，并添加到窗口

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
