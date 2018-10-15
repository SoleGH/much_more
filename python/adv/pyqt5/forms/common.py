# -*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel
from PyQt5 import QtCore


class CaptchaLabel(QLabel):
    def __init__(self, parent=None):
        super(CaptchaLabel, self).__init__(parent)

    def mousePressEvent(self, e):  # 重载一下鼠标点击事件
        print("click captcha")
        # get_captcha()
        self.setPixmap(QPixmap("./captcha.png"))


def show_captcha(obj, window, site_size):
    setattr(obj, 'captcha_img', CaptchaLabel(window))
    captcha_obj = getattr(obj, 'captcha_img')
    captcha_obj.setPixmap(QPixmap("./captcha.png"))
    captcha_obj.setGeometry(QtCore.QRect(*site_size))


def update_captcha(obj):
    # get_captcha()
    captcha_obj = getattr(obj, 'captcha_img')
    captcha_obj.setPixmap(QPixmap("./captcha.png"))


def get_label_key(_name):
    return "{}_label".format(_name)


def get_edit_box_key(_name):
    return "{}_edit".format(_name)


def get_btn_key(_name):
    return "{}_btn".format(_name)

