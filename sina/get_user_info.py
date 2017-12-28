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


def get_user_info(user_id):
    user_id = str(user_id)
    user_url = "https://weibo.cn/" + user_id
    try:
        html = requests.get(user_url, headers=get_head())
        content = str(html.content)

        if len(content) == 0:
            print "微博反爬虫，等待1分钟"
            return None
        try:
            results = re.findall(r"微博\[.*?\]", content, re.I | re.S | re.M)
            post_num = results[0].replace("微博[", "").replace("]", "")

            results = re.findall(r"粉丝\[.*?\]", content, re.I | re.S | re.M)
            fllower_num = results[0].replace("粉丝[", "").replace("]", "")

            results = re.findall(r"关注\[.*?\]", content, re.I | re.S | re.M)
            fllowee_num = results[0].replace("关注[", "").replace("]", "")

            results = re.findall(r"<title>.*?</title>", content, re.I | re.S | re.M)
            user_name = results[0].replace("<title>", "").replace("的微博</title>", "").encode('UTF-8')

            sql = "INSERT INTO user_info VALUES ( '%s','%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE USER_NAME = '%s',USER_URL = '%s',FLLOWER_NUM='%s',FLLOWEE_NUM='%s',POST_NUM='%s'" \
                  % (user_id, user_name, user_url, fllower_num, fllowee_num, post_num, "false", user_name,
                     user_url, fllower_num, fllowee_num,
                     post_num)

            MySQLClient.execute(sql)
        except Exception, e:
            print e
            MySQLClient.update("UPDATE user_info SET USER_URL = 'error' WHERE USER_ID = '" + user_id + "'")
            return None

        return "success"

    except Exception, e:
        print e


def start_get_user_info():
    while True:
        user_id = MySQLClient.fetchone("SELECT USER_ID FROM user_info WHERE USER_URL is NULL ")[0]
        if get_user_info(user_id) is None:
            time.sleep(10)
            change_cookie()
            continue
        print str(user_id) + "的用户信息已获取完成"


start_get_user_info()
