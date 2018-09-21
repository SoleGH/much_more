# _*_ utf-8 _*_
import sqlite3
from contextlib import contextmanager

from common.const import CONST
from common.loggers.logger import log


class SqlLiteTool(object):
    def __init__(self):
        self.conn = None
        self.cursor = None

        self.init_db()

    def __get_conn(self, db_name="main.db"):
        if not self.conn:
            self.conn = sqlite3.connect(CONST.PROJECT_PATH + CONST.LOG_STORAGE_PATH + db_name)

    def __get_cursor(self, conn):
        if not self.cursor:
            self.cursor = conn.cursor

    @contextmanager
    def get_session(self):
        try:
            self.__get_conn()
            self.__get_cursor(self.conn)
            yield self.cursor
            self.conn.commit()
        except Exception as e:
            log.exception(e)
        finally:
            if self.conn:
                self.conn.rollback()
                self.conn.close()

    def execute(self, sql_str):
        with self.get_session() as session:
            result = session.excute(sql_str)
        return result

    def init_db(self):
        create_cache = "create table if not exists cache(id int auto_increment primary key not null, " \
              "name varchar(20) unique, value varchar(256);"
        with self.get_session() as session:
            result = session.execute(create_cache)
        return result


sql_lite_tool = SqlLiteTool()
