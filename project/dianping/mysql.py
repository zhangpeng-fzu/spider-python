# -*-coding:utf8-*-

import sys
import MySQLdb

reload(sys)

sys.setdefaultencoding('utf-8')


class MySQL(object):
    def __init__(self):
        self.host = 'localhost'
        self.user = 'root'
        self.passwd = 'admin'
        self.port = 3306
        self.table = "dianping"

        self.db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port,
                                  charset='utf8')
        self.db.select_db(self.table)
        self.cursor = self.db.cursor()

    def set_table(self, table):
        self.table = table
        self.db.select_db(table)
        self.cursor = self.db.cursor()

    def execute(self, sqlstr):
        try:
            # 提交到数据库执行
            count = self.cursor.execute(sqlstr)
            self.db.commit()
            return count

        except Exception as e:
            print(e)

    def update(self, sqlstr):
        try:
            # 提交到数据库执行
            self.cursor.execute(sqlstr)
            self.db.commit()
        except Exception as e:
            print(e)

    def fetchone(self, sqlstr):
        try:
            self.execute(sqlstr)
            return self.cursor.fetchone()
        except Exception as e:
            print(e)

    def fetchmany(self, sqlstr):
        try:
            record = self.execute(sqlstr)
            return self.cursor.fetchmany(record)
        except Exception as e:
            print(e)

    def close(self):
        self.cursor.close()
        self.db.close()
