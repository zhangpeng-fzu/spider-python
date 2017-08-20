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
        self.table = "itslaw"

        self.db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, port=self.port,
                                  charset='utf8')
        self.db.select_db(self.table)
        self.cursor = self.db.cursor()

    def set_table(self, table):
        self.table = table
        self.db.select_db(table)
        self.cursor = self.db.cursor()

    def execute(self, sql):
        try:
            # 提交到数据库执行
            return self.cursor.execute(sql)
        except Exception, e:
            print(e)

    def fetchone(self, sql):
        try:
            self.execute(sql)
            return self.cursor.fetchone()
        except Exception, e:
            print(e)

    def fetchmany(self, sql):
        try:
            record = self.execute(sql)
            return self.cursor.fetchmany(record)
        except Exception, e:
            print(e)

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == "__main__":
    MySQLClient = MySQL()
    MySQLClient.set_table("itslaw")
    sql = "select count(*) from JUGEMENT"
    print(MySQLClient.fetchone(sql)[0])
    MySQLClient.close()
