# -*-coding:utf8-*-

import sys
import re
import requests
import time
from cookie_manager import *
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("weibo")


# 获取粉丝列表
# 由于微博智能反垃圾列表，会导致抓取的粉丝数少于显示数量
def get_fllower(user_id, page):
    print "正在获取%s的第%s页粉丝数据" % (user_id, page)
    user_url = "https://weibo.cn/%s/fans?page=%s" % (user_id, page)
    try:
        html = requests.get(user_url, headers=get_head())
        content = str(html.content)
        if len(content) == 0:
            print "获取粉丝列表失败"
            return None

        user_ids = re.findall(r"add\?uid=.*?&", content, re.I | re.S | re.M)

        if len(user_ids) == 0:
            return None

        print "成功获取%s条粉丝id" % len(user_ids)
        for fllower_id in user_ids:
            fllower_id = fllower_id.replace("add?uid=", "").replace("&", "")
            if fllower_id == user_id:
                continue
            sql = "INSERT INTO fllower VALUES ('%s','%s')" % (user_id, fllower_id)
            MySQLClient.execute(sql)

            sql = "INSERT INTO user_info( USER_ID ) VALUES ('%s')" % fllower_id
            MySQLClient.execute(sql)
        return "success"

    except Exception, e:
        print e  # 获取关注列表


# 由于微博智能反垃圾列表，会导致抓取的粉丝数少于显示数量
def get_fllowee(user_id, page):
    print "正在获取%s的第%s页关注数据" % (user_id, page)
    user_url = "https://weibo.cn/%s/follow?page=%s" % (user_id, page)
    try:
        html = requests.get(user_url, headers=get_head())
        content = str(html.content)

        if len(content) == 0:
            print "微博反爬虫，等待1分钟"
            return None

        user_ids = re.findall(r"add\?uid=.*?&", content, re.I | re.S | re.M)

        if len(user_ids) == 0:
            return None
        print "成功获取%s条关注者id" % len(user_ids)
        for fllowee_id in user_ids:
            fllowee_id = fllowee_id.replace("add?uid=", "").replace("&", "")
            if fllowee_id == user_id:
                continue

            sql = "INSERT INTO fllowee VALUES ('%s','%s')" % (
                user_id, fllowee_id)
            MySQLClient.execute(sql)

            sql = "INSERT INTO user_info( USER_ID ) VALUES ('%s')" % fllowee_id
            MySQLClient.execute(sql)
        return "success"

    except Exception, e:
        print e


def start_id_generator(seed_id):
    user_id = seed_id
    count = 0
    while user_id is not None and int(count) <= 20000:
        user_id = str(user_id)
        for i in range(20):
            if get_fllowee(user_id, i + 1) is None or get_fllower(user_id, i + 1) is None:
                time.sleep(10)
                change_cookie()
                continue

        MySQLClient.update("UPDATE user_info SET IS_UPDATE = 'true' WHERE USER_ID = '" + user_id + "'")
        user_id = MySQLClient.fetchone("SELECT USER_ID FROM user_info WHERE IS_UPDATE != 'true' ")[0]
        count = MySQLClient.fetchone("select count(*) from user_info")[0]
        print "%s的粉丝和关注列表获取完成" % user_id


start_id_generator("2093492691")
