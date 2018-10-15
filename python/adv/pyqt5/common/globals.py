# -*- coding:utf-8 -*-
from common.singleton import Singleton


class __Globals(metaclass=Singleton):
    def __init__(self):
        self.__is_running = False
        self.__refresh_run_status = False

    def get_is_running(self):
        return self.__is_running

    def set_is_running(self, _is_running):
        self.__is_running = _is_running

    def get_refresh_run_status(self):
        return self.__refresh_run_status

    def set_refresh_run_status(self, _refresh_run_status):
        self.__refresh_run_status = _refresh_run_status


Globals = __Globals()
