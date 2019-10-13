# -*-coding:utf-8-*-

import pymysql
import oss2

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'zhenai',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)


# 获取数据库连接
def init_connection():
    return connection


# 获取oss bucket
def init_bucket():
    auth = oss2.Auth('LTAInxELbFWfNSjr', 'Nu0UxZpZcpNBeJJAfvLRKUgmSARZFV')
    bucket = oss2.Bucket(auth, 'oss-cn-hangzhou.aliyuncs.com', 'xxroom')
    return bucket
