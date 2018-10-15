# -*- coding: utf-8 -*-

from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QWidget, QLabel, QPushButton

from common.const import CONST
from common.xml_utils import set_or_update, get_node_content
from forms.MyQWidget import MyQWidget
from forms.base_ui import BaseUI
from forms.common import show_captcha, update_captcha, get_edit_box_key
from common.logger import log
from common.globals import Globals


icon_path = './image/logo.png'  # exe
# icon_path = './resource/image/logo.png'


class ErrorUI(BaseUI):
    def __init__(self):
        self.main_ui = QWidget()
        self.main_ui.setWindowIcon(QIcon(icon_path))

        self.main_ui.setWindowTitle('MWS')
        self.main_ui.resize(200, 100)
        self.main_ui.move(self.get_top_left(self.main_ui))  # 窗口居中
        self.main_ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶

        self.label = QLabel('请不要重复运行!', self.main_ui)
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.setGeometry(QtCore.QRect(43, 5, 100, 30))

        self.btn = QPushButton('OK', self.main_ui)
        self.btn.setGeometry(QtCore.QRect(70, 55, 50, 30))
        self.btn.clicked.connect(QCoreApplication.instance().quit)  # 点击关闭窗口
        self.main_ui.show()


class MainUI(BaseUI):
    def __init__(self):
        self.main_ui = MyQWidget()
        self.main_ui.setWindowIcon(QIcon(icon_path))
        self.init_main_ui()

        self.main_ui.move(self.get_top_left(self.main_ui))  # 窗口居中
        # self.main_ui.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)  # 置顶

    def init_main_ui(self):
        # TODO 自动登录
        login_status = False
        if login_status:
            set_or_update(CONST.SAAS_LOGIN_TAG, 'TRUE')
            run_status = get_node_content(CONST.RUN_STATUS)
            if run_status == CONST.AUTHENTICATED:
                self.add_run_page_modules()
            else:
                self.add_second_page_modules()
        else:
            self.add_saas_page_modules()
        self.main_ui.show()

    def add_saas_page_modules(self):
        self.main_ui.resize(290, 180)
        self.main_ui.setWindowTitle('page2')
        # 邮箱录入框
        self.add_label_edit(self.main_ui, 'test', 'test', 0, 60)

        # 按钮
        saas_login_btn = self.add_button(self.main_ui, 'login','login', (105, 120, 80, 30))
        saas_login_btn.clicked.connect(self.login)

        # TODO 获取验证码并展示
        # get_captcha()
        # show_captcha(self, self.main_ui, (130, 80, 100, 28))  # (left,top,width,high)

    def remove_saas_page_modules(self):
        name_type_list = [('test', CONST.EDIT), ('login', CONST.BUTTON)]
        self.remove_module_many(name_type_list)

    def add_second_page_modules(self):
        self.main_ui.resize(290, 180)
        self.main_ui.setWindowTitle('page2')

        self.add_label_edit(self.main_ui, 'test', 'test', 0)

        back_login_btn_name = 'back_login'
        back_login_btn = self.add_button(self.main_ui, back_login_btn_name, back_login_btn_name, (60, 120, 80, 30))
        back_login_btn.clicked.connect(self.back_login)

        next_page = 'next'
        next_btn = self.add_button(self.main_ui, next_page, next_page, (170, 120, 80, 30))
        next_btn.clicked.connect(self.next_page)

    def remove_second_page_modules(self):
        name_type_list = [('test', CONST.EDIT), ('back_login', CONST.BUTTON),
                          ('next', CONST.BUTTON)]
        self.remove_module_many(name_type_list)

    def add_run_page_modules(self):
        self.main_ui.resize(290, 230)
        self.main_ui.setWindowTitle('page3')
        version = 'version'
        run_status = 'status'
        task1_status = 'task1'

        left = (35, 135)
        self.add_label_edit(self.main_ui, version, version, 0, 60, left=left)
        self.update_edit_text(version, '0')
        self.disable_edit_text(version)

        self.add_label_edit(self.main_ui, run_status, run_status, 1, 60, left=left)
        self.update_edit_text(run_status, '正常')
        self.disable_edit_text(run_status)
        run_status_edit_box_obj = getattr(self, get_edit_box_key(run_status))
        run_status_edit_box_obj.textChanged.connect(self.check_run_status)

        self.add_label_edit(self.main_ui, task1_status, task1_status, 2, 60, left=left)
        self.update_edit_text(task1_status, '暂无')
        self.disable_edit_text(task1_status)

        Globals.set_refresh_run_status(True)
        # threading.Thread(target=sync_status, args=(self,)).start()

        pre = 'pre'
        cancel_authorize_btn = self.add_button(self.main_ui, pre,
                                               pre, (110, 150, 80, 30))
        cancel_authorize_btn.clicked.connect(self.pre_page)

    def remove_three_page_modules(self):
        name_type_list = [('version', CONST.EDIT), ('status', CONST.EDIT),
                          ('task1', CONST.EDIT), ('pre', CONST.BUTTON)]
        self.remove_module_many(name_type_list)

    def back_login(self):
        # TODO 退出登录, 并页面跳转
        self.main_ui.hide()
        self.remove_second_page_modules()
        self.add_saas_page_modules()
        self.main_ui.show()

    def check_run_status(self):
        run_status = get_node_content(CONST.RUN_STATUS)
        print("text changed:{}".format(run_status))
        if run_status == CONST.INVALID:
            reply = QMessageBox.information(self.main_ui, 'Message', '任务失败')
            if reply == QMessageBox.Ok:
                self.pre_page()

    def next_page(self):
        err_info = False
        if err_info:
            QMessageBox.information(self.main_ui, '跳转失败', '跳转失败')
        else:
            self.main_ui.hide()
            self.remove_second_page_modules()
            self.add_run_page_modules()
            self.main_ui.show()

    def pre_page(self):
        self.main_ui.hide()
        self.remove_three_page_modules()
        self.add_second_page_modules()
        self.main_ui.show()

    def login(self):
        try:
            info = None

            already_login = False
            if not already_login:
                # email = self.get_edit_text(EMAIL_TAG)
                # password = self.get_edit_text(PW_TAG)
                # captcha = self.get_edit_text(CAPTCHA_TAG)
                # TODO 登录
                # already_login, err_code, info = login(email, password, captcha)
                already_login = True

            if already_login:
                self.main_ui.hide()
                self.remove_saas_page_modules()
                self.add_second_page_modules()
                self.main_ui.show()
            else:
                QMessageBox.information(self.main_ui, '登录失败', info)
                update_captcha(self)
        except Exception as err:
            log.exception(err)
