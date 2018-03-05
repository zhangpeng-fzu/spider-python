# -*-coding:utf-8-*-

import pymysql

head = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/people/xu-chen-hao-9-24/activities",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20",
    # 操作cookie
    "Cookie": 'aliyungf_tc=AQAAAGqNpwMtXAQAwwsjeC+Ws4nuRuQM; _xsrf=fe6774a0-913e-4dac-b949-e76a1304790c; q_c1=8008992a5439454d80034f17745e3f00|1519895601000|1519895601000; _zap=fede0ae4-2500-4aec-ad8c-d295c77b4d93; l_n_c=1; l_cap_id="ZjI2YTMxNGU4Y2IzNDRlODg3ODQ1MmI5MWVlODEwMDU=|1519895606|3d3793ae69f9f9e45336b100da5c7d29eae53b77"; r_cap_id="YzFkNzU5NjdmZDUzNDEzZTkwZjI0OGU1ZDNhZTgzM2Q=|1519895606|ede5d7f2d7a96c68ab48ced2147207d9156a722f"; cap_id="ZWQ4ODMyODA5OGQyNDUyZDhjMGNkYWJhYzY1ZThkOTc=|1519895606|ded435dd86c3ee222fd301b81e83187638bd761b"; n_c=1; d_c0="AADtA5W9Ow2PTiN6eigkl7Dt010OlHYhVrI=|1520127420"'
}

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'db': 'zhihu',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)

# 爬取用户数量
max_user_num = 100000


def init_connection():
    return connection


def get_head():
    return head
