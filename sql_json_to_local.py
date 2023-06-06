# -*- coding:utf-8 -*-
import json

from pymysql import connect
from datetime import datetime


def format_timestamp(timestamp):
    date_time = datetime.fromtimestamp(timestamp)
    date_time_str = date_time.strftime('%Y-%m-%d %H:%M:%S')
    return date_time_str


def connect_db():
    # db = connect(host='192.168.0.117',
    #              user='yiguo',
    #              password='f5d96f1fde843964b9ff8a7003b7face60bc9952',
    #              database='ygbilling_db',
    #              charset='utf8')
    db = connect(host='192.168.0.213',
                 user='root',
                 password='123456',
                 database='test_db',
                 charset='utf8')
    cursor = db.cursor()
    return cursor, db


class Export(object):
    def __init__(self, cursor, db, file_fall_name=None):
        self.cursor = cursor
        self.db = db
        self.file_fall_name = file_fall_name
        self.offset = 0
        self.size = 256
        self.sub_list = None

    def end(self):
        self.cursor.close()
        self.db.close()

    def get_lessee_list(self):
        sql = "select company_name,create_date,lessee_uid from dzh_saaslessee;"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def get_sub_list(self):
        # TODO 分页查询 limint offset,size
        sql = "select subaccount_uid,nickname,phone,email,last_login_date from dzh_subaccount limit {},{};".format(
            self.offset, self.size)
        self.cursor.execute(sql)
        self.sub_list = self.cursor.fetchall()

    def get_lessee_by_sid(self, sid):
        lessee_uid = sid[:16]
        sql = "select company_name,create_date from dzh_saaslessee where lessee_uid = '{}';".format(lessee_uid)
        self.cursor.execute(sql)
        result = self.cursor.fetchone()
        return result

    def get_detail(self):
        records_dict = {}
        for sub_tuple in self.sub_list:
            sid = sub_tuple[0]
            lessee_tuple = self.get_lessee_by_sid(sid)
            if not lessee_tuple:
                continue
            record = {
                "company_name": lessee_tuple[0],
                "create_date": lessee_tuple[1],
                "nickname": sub_tuple[1],
                "phone": sub_tuple[2],
                "email": sub_tuple[3]
            }
            if sub_tuple[4]:
                record["last_login_date"] = format_timestamp(sub_tuple[4])
            else:
                record["last_login_date"] = sub_tuple[4]
            records_dict[sid] = record

        return records_dict

    def save_records(self):
        count = 0
        while True:
            self.get_sub_list()
            if not self.sub_list:
                break
            self.offset = self.offset + self.size
            data = self.get_detail()
            file_name = self.file_fall_name if self.file_fall_name else './users.json'
            print(file_name)
            with open(file_name, 'a') as f:
                count += len(data)
                for key in data.keys():
                    str = "{'%s':%s}" % (key, json.dumps(data[key], ensure_ascii=False,))

                    f.write(str + '\n')
                # json.dump(data, f, ensure_ascii=False, indent=4)
        print("total count:{}".format(count))


if __name__ == "__main__":
    cursor, db = connect_db()
    export = Export(cursor, db)
    export.save_records()
