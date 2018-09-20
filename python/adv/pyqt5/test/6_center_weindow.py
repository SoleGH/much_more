#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This program centers a window
on the screen.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        self.resize(250, 150)
        self.center()

        self.setWindowTitle('Center')
        self.show()

    def center(self):

        qr = self.frameGeometry()  # 获取主窗体大小
        cp = QDesktopWidget().availableGeometry().center()  # 显示器的分辨率，然后得到中间点的位置。
        qr.moveCenter(cp)  # 主窗体移动到中心位置,目的是获取中心位置左上角坐标
        self.move(qr.topLeft())  # 把窗口的坐上角的坐标设置为qr的矩形左上角的坐标


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())