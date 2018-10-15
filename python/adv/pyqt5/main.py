# *_* uft-8 *_*
import os
import winreg
from PyQt5.QtWidgets import QApplication
import sys
# 设置项目路径必须在本地包导入最顶层
from common.const import CONST
current_file = os.path.abspath(__file__)
main_dir = os.path.dirname(current_file)
CONST.PROJECT_PATH = main_dir
from forms.main_ui import MainUI, ErrorUI

from common.logger import log
from common.xml_utils import set_or_update, get_node_content


def storage_main_app_name():
    file_name = os.path.basename(__file__).split('.')[0]
    set_or_update(CONST.MAIN_APP_NAME_TAG, file_name)


def add_to_win_register():
    sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
    register_value_part = os.path.abspath(__file__).split('.')[0]
    log.info("value:{}".format(register_value_part))
    value = '"{}.exe" /start'.format(register_value_part)

    log.info("add register path:{},value:{}".format(sub_key, value))
    reg_keys = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, sub_key, 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(reg_keys, 'a_test_register_main', 0, winreg.REG_SZ, value)


def app_is_run():
    try:
        return False
    except Exception as err:
        log.exception(err)


def main():
    try:
        app = QApplication(sys.argv)
        if app_is_run():
            ex = ErrorUI()
        else:
            ex = MainUI()
        sys.exit(app.exec_())
    except Exception as e:
        log.exception(e)


if __name__ == '__main__':
    main()