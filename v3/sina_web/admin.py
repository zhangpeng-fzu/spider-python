# _*_coding:utf-8_*_

import collections
import json

import db

connection = db.get_connection()


def findOne(account):
    try:
        user = {}
        with connection.cursor() as cursor:
            sql = "SELECT * from users WHERE account = '" + str.strip(account) + "'"
            cursor.execute(sql)
            row = cursor.fetchone()  # 获取查询的所有记录
            if row is None:
                return None
            # 遍历结果
            user['account'] = row["ACCOUNT"]
            user['password'] = row["PASSWORD"]
            user['role'] = row["ROLE"]
        return user

    except Exception as e:
        print("数据库获取列表失败", e)


def get_list():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * from users'
            cursor.execute(sql)
            rows = cursor.fetchall()  # 获取查询的所有记录
            result = {}
            # 遍历结果
            objects_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['account'] = row["ACCOUNT"]
                d['role'] = row["ROLE"]
                d['createTime'] = str(row["CREATE_TIME"])
                objects_list.append(d)
            result["data"] = objects_list
            return json.dumps(result)

    except Exception as e:
        print("数据库获取列表失败", e)


if __name__ == '__main__':
    findOne("admin")
