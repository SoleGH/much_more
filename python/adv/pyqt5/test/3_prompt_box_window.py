#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This example shows a tooltip on
a window and a button.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QToolTip, QPushButton)
from PyQt5.QtGui import QFont


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))  # 设置提示框字体

        self.setToolTip('This is a <b>QWidget</b> widget')  # 整个窗体提示信息

        btn = QPushButton('Button', self)  # 设置按钮
        btn.setToolTip('This is a <b>QPushButton</b> widget')  # 设置按钮提示内容
        btn.resize(btn.sizeHint())  # 设置案例尺寸， sizeHint()提供默认按钮大小
        btn.move(50, 50)  # 设置按钮位置

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Tooltips')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())