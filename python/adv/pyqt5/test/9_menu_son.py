#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
ZetCode PyQt5 tutorial

This program creates a submenu.

Author: Jan Bodnar
Website: zetcode.com
Last edited: August 2017
"""

import sys
from PyQt5.QtWidgets import QMainWindow, QAction, QMenu, QApplication


class Example(QMainWindow):

    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):

        menubar = self.menuBar()  # 获取菜单栏
        fileMenu = menubar.addMenu('File')  # 添加一级菜单file

        impMenu = QMenu('Import', self)  # 创建新菜单（这里为二级）
        impAct = QAction('Import mail', self)  # 创建新功能
        impMenu.addAction(impAct)  # import菜单添加功能import email

        newAct = QAction('New', self)  # 创建功能

        fileMenu.addAction(newAct)  # 一级菜单添加功能
        fileMenu.addMenu(impMenu)  # 一级菜单添加二级菜单

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Submenu')
        self.show()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())