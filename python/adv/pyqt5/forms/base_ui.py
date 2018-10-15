# -*- coding: utf-8 -*-
from PyQt5 import sip, QtCore
from PyQt5.QtWidgets import QLabel, QLineEdit, QDesktopWidget, QPushButton

from common.const import CONST
from common.logger import log
from forms.common import get_label_key, get_edit_box_key, get_btn_key


class BaseUI(object):
    @classmethod
    def get_top_left(cls, window_obj):
        qr = window_obj.frameGeometry()  # 获取窗体大小
        cp = QDesktopWidget().availableGeometry().center()  # 显示器的分辨率，然后得到中间点的位置。
        qr.moveCenter(cp)  # 主窗体移动到中心位置,目的是获取中心位置左上角坐标
        return qr.topLeft()

    def add_label(self, window_obj, label_en, label_zh, site_size):
        label_key = get_label_key(label_en)
        setattr(self, label_key, QLabel('{}:'.format(label_zh), window_obj))
        label_obj = getattr(self, label_key)
        label_obj.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        label_obj.setGeometry(QtCore.QRect(*site_size))

    def add_edit_box(self, window_obj, label_en, site_size):
        edit_key = get_edit_box_key(label_en)
        setattr(self, edit_key, QLineEdit(window_obj))
        edit_obj = getattr(self, edit_key)
        edit_obj.setGeometry(QtCore.QRect(*site_size))

    def update_edit_text(self, edit_name, text):
        edit_key = get_edit_box_key(edit_name)
        edit_obj = getattr(self, edit_key)
        if edit_obj:
            edit_obj.setText(text)

    def disable_edit_text(self, edit_name):
        edit_key = get_edit_box_key(edit_name)
        edit_obj = getattr(self, edit_key)
        if edit_obj:
            edit_obj.setEnabled(False)

    def get_edit_text(self, edit_name):
        edit_key = get_edit_box_key(edit_name)
        edit_obj = getattr(self, edit_key)
        return edit_obj.text()

    def add_button(self, window_obj, button_name, button_comment, site_size):
        button_key = get_btn_key(button_name)
        setattr(self, button_key, QPushButton(button_comment, window_obj))
        btn_module = getattr(self, button_key)
        btn_module.setGeometry(QtCore.QRect(*site_size))
        return btn_module

    def add_label_edit(self, window_obj, label_en, label_zh, no, label_width=100, edit_width=150, left=(15, 115)):
        # 封装添加录入项

        label_site_size = (left[0], 18 + (30 * no), label_width, 25)  # （left,top,width,high）
        edit_site_size = (left[1] + (label_width - 100), 23 + (30 * no), edit_width, 25)

        self.add_label(window_obj, label_en, label_zh, label_site_size)
        self.add_edit_box(window_obj, label_en, edit_site_size)

    def remove_module(self, _name, module_type=None):
        """
        删除已经绘制的QT组件
        module_type为edit（输入框）时，自动删除对应的label标题
        :param _name: 组件名称
        :param module_type: 组件类型：edit,label,button
        :return:
        """
        key_list = []
        if module_type == CONST.LABEL:
            key_list.append(get_label_key(_name))
        elif module_type == CONST.BUTTON:
            key_list.append(get_btn_key(_name))
        elif module_type == CONST.EDIT:
            key_list.append(get_label_key(_name))
            key_list.append(get_edit_box_key(_name))
        else:
            key_list.append(_name)

        for key in key_list:
            module = getattr(self, key, None)
            if module:
                sip.delete(module)
                setattr(self, key, None)

    def remove_module_many(self, name_type_list):
        try:
            for key, module_type in name_type_list:
                self.remove_module(key, module_type)
        except Exception as err:
            log.exception(err)
