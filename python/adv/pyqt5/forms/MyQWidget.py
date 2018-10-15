# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import QWidget, QMessageBox

from common.globals import Globals
from common.logger import log


class MyQWidget(QWidget):
    def __init__(self):
        super().__init__()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                     QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            Globals.set_is_running(False)
            log.info("close windows")
        else:
            event.ignore()
