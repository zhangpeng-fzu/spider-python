# _*_coding:utf-8_*_

from pymysqlpool import ConnectionPool

# 数据库配置
config = {
    'pool_name': 'news',
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',  # 数据库密码
    'db': 'sina_news',
    'charset': 'utf8'
}

pool = ConnectionPool(**config)


def get_connection():
    # Return a connection pool instance
    pool.connect()
    return pool
