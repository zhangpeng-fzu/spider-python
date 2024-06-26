# -*-coding:utf8-*-

import re
import sys
import time

import requests
from cookie_manager import *

from common.database import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("weibo")


def get_user_info(user_id):
    user_id = str(user_id)
    user_url = "https://weibo.cn/" + user_id
    print("正在获取%s的用户信息" % user_id)
    try:
        html = requests.get(user_url, headers=get_head())
        content = str(html.content)

        if len(content) == 0:
            print("微博反爬虫，等待1分钟")
            return None
        try:
            results = re.findall(r"微博\[.*?\]", content, re.I | re.S | re.M)
            if len(results) != 0:
                post_num = results[0].replace("微博[", "").replace("]", "")
            else:
                post_num = 0

            results = re.findall(r"粉丝\[.*?\]", content, re.I | re.S | re.M)
            if len(results) != 0:
                fllower_num = results[0].replace("粉丝[", "").replace("]", "")
            else:
                fllower_num = 0

            results = re.findall(r"关注\[.*?\]", content, re.I | re.S | re.M)
            if len(results) != 0:
                fllowee_num = results[0].replace("关注[", "").replace("]", "")
            else:
                fllowee_num = 0

            results = re.findall(r"<title>.*?</title>", content, re.I | re.S | re.M)
            try:
                if len(results) != 0:
                    user_name = results[0].replace("<title>", "").replace("的微博</title>", "").encode("utf-8")
                else:
                    user_name = ""
            except Exception as e:
                user_name = ""

            print("%s的用户名为%s" % (user_id, user_name))

            sql = "INSERT INTO user_info VALUES ( '%s','%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE USER_NAME = '%s',USER_URL = '%s',FLLOWER_NUM='%s',FLLOWEE_NUM='%s',POST_NUM='%s'" \
                  % (
                      user_id, user_name.encode("utf-8"), user_url, fllower_num, fllowee_num, post_num, "false",
                      user_name,
                      user_url, fllower_num, fllowee_num,
                      post_num)

            MySQLClient.execute(sql)
        except Exception as e:
            print(e)
            MySQLClient.update("UPDATE user_info SET USER_URL = 'error' WHERE USER_ID = '" + user_id + "'")
            return None

        return "success"

    except Exception as e:
        print(e)


def start_get_user_info():
    while True:
        user_id = MySQLClient.fetchone("SELECT USER_ID FROM user_info WHERE USER_URL is NULL ")[0]
        if get_user_info(user_id) is None:
            time.sleep(30)
            change_cookie()
            continue
        print(str(user_id) + "的用户信息已获取完成")


start_get_user_info()
