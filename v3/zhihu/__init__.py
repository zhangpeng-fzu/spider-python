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
    "Cookie": 'd_c0="AJBC0WuMYguPTnaNiCFdE0xoch7KKC2mhAU=|1488372040"; _zap=b00dea6a-dd36-4aa0-baec-36e0f8d0fe7b; q_c1=e7e0740fcece4a4ba85bd08d93c6d6d1|1506351455000|1488372020000; aliyungf_tc=AQAAADsLUmcxFwkAYVRNfRMb03d+mrIo; _xsrf=10fc75da-cf1a-4b60-850b-aa4ec51055fc; q_c1=e7e0740fcece4a4ba85bd08d93c6d6d1|1520045042000|1488372020000; r_cap_id="NTAzN2QwZDFkODVmNDhlMThmMDg5NDlkNDQwNmZlYjM=|1520045057|406ea0223d1c6db344b3baf71260d52c2a7d8721"; cap_id="MjEyZTU1MzY4OGRlNGQyZjhkZTBkY2IwZGM4ODI1ZDY=|1520045057|b25ba13b566449626a03121f03012d8112769660"; l_cap_id="NTkyNmZmNzIxOGYwNDVlYWE0N2Q5Nzc5NGI2NzAwYzQ=|1520045057|256dbd6180ab911d69522af5753fb95dfd0c3977"; __utmc=155987696; __utmz=155987696.1520046650.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=155987696.1329378831.1520046650.1520060741.1520067528.3; anc_cap_id=e36d2981df9147139220dcd3cd92cd5a; capsion_ticket="2|1:0|10:1520085147|14:capsion_ticket|44:MWFmMTZkM2VkNzM3NDEwM2ExYWY3NTgwYjhjNmEwMTQ=|2ec10945c82b6deb35292faaa0e2f9c437f22e6f32e10a05fa3ad31b66ec5046"',
}

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'db': 'zhihu',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)


def init_connection():
    return connection


def get_head():
    return head
