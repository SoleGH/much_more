# *_* uft-8 *_*
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit, QInputDialog, QApplication, QDesktopWidget, QLabel)
import sys


def get_captcha():
    url = 'http://192.168.0.16/ygdzh/api/v1/register/query_captcha'
    res = requests.get(url)
    res.encoding = 'utf-8'
    img = res.content
    with open('captcha.png', 'wb') as file:
        file.write(img)
        file.close()


class CaptchaLabel(QLabel):
    def __init__(self, parent=None):
        super(CaptchaLabel, self).__init__(parent)

    def mousePressEvent(self, e):  # 重载一下鼠标点击事件
        print("click captcha")
        get_captcha()
        self.setPixmap(QPixmap("./captcha.png"))


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def get_top_left(self):
        qr = self.frameGeometry()  # 获取主窗体大小
        cp = QDesktopWidget().availableGeometry().center()  # 显示器的分辨率，然后得到中间点的位置。
        qr.moveCenter(cp)  # 主窗体移动到中心位置,目的是获取中心位置左上角坐标
        return qr.topLeft()

    def add_label(self, label_en, label_zh, no):
        label = "{}_label".format(label_en)
        setattr(self, label, QLabel('{}:'.format(label_zh), self))
        label_obj = getattr(self, label)
        label_obj.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        label_obj.resize(50, 15)
        label_obj.move(20, 23 + (25 * no))

    def add_edit_box(self, label_en, no, edit_len=None):
        edit = "{}_edit".format(label_en)
        setattr(self, edit, QLineEdit(self))
        edit_obj = getattr(self, edit)
        edit_obj.move(70, 20 + (25 * no))
        if edit_len:
            edit_obj.resize(edit_len, 25)

    def add_label_edit(self, label_en, label_zh, no):
        # 封装添加录入项
        self.add_label(label_en, label_zh, no)
        self.add_edit_box(label_en, no)

    def init_ui(self):
        # 邮箱录入框
        self.add_label_edit('email', '邮箱', 0)
        self.add_label_edit('pw', '密码是', 1)
        self.add_label('captcha', '验证码', 2)
        self.add_edit_box('captcha', 2, 50)

        # 按钮
        setattr(self, 'btn', QPushButton('saas login', self))
        self.btn.move(80, 120)
        self.btn.clicked.connect(self.show_dialog)

        self.show_captcha()

        self.resize(250, 500)
        self.setWindowTitle('saas login')
        self.move(self.get_top_left())
        self.show()

    def show_captcha(self):
        setattr(self, 'captcha_img', CaptchaLabel(self))
        captcha_obj = getattr(self, 'captcha_img')
        captcha_obj.setPixmap(QPixmap("./captcha.png"))
        captcha_obj.resize(100, 30)
        captcha_obj.move(130, 75)

    def show_dialog(self):
        text, ok = QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')

        if ok:
            self.le.setText(str(text))


if __name__ == '__main__':
    get_captcha()
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
