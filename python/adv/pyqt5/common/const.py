# -*- coding:utf-8 -*-
import os


class _CONST(object):
    def __init__(self):
        # 设置项目路径
        current_path = os.path.abspath(__file__)
        project_path = os.path.abspath(os.path.dirname(current_path) + os.path.sep + ".")
        self.PROJECT_PATH = project_path + '/../'

    def __setattr__(self, *_):
        if _[0] != "PROJECT_PATH":
            raise SyntaxError('Trying to change a constant value')
        super.__setattr__(self, *_)

    SYSTEM_NAME = "tool"
    LOG_STORAGE_PATH = "/data/log/"
    DB_DIR = "/data/db/"
    DZH_SERVER_HOST = "192.168.0.16"
    DZH_SERVER_PORT = 80


CONST = _CONST()
