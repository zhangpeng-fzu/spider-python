# -*-coding:utf8-*-

import sys
import time
import re
import requests
from cookie_manager import *
from urllib import urlencode
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("weibo")


def parse_weibo(weibo_data, user_id):
    is_forward = "false"
    weibo_id = weibo_data.split(">")[0].replace("=", "").replace("\"", "")
    results = re.findall(r"class=\"ctt\">.*?赞", weibo_data, re.I | re.S | re.M)
    if len(results) != 0:
        weibo_content = results[0].replace("class=\"ctt\">", "").replace("赞", "")
    else:
        weibo_content = ""

    results = re.findall(r"赞\[.*?\]", weibo_data, re.I | re.S | re.M)
    if len(results) != 0:
        weibo_zan_num = results[0].replace("赞[", "").replace("]", "")
    else:
        weibo_zan_num = 0

    results = re.findall(r"评论\[.*?\]", weibo_data, re.I | re.S | re.M)

    if len(results) != 0:
        weibo_comment_num = results[0].replace("评论[", "").replace("]", "")
    else:
        weibo_comment_num = 0

    results = re.findall(r"转发\[.*?\]", weibo_data, re.I | re.S | re.M)

    if len(results) != 0:
        weibo_forward_num = results[0].replace("转发[", "").replace("]", "")
    else:
        weibo_forward_num = 0

    if "转发了" in weibo_data:
        is_forward = "true"

    results = re.findall(r"class=\"ct\">.*?来自", weibo_data, re.I | re.S | re.M)
    post_time = results[0].replace("class=\"ct\">", "").replace("&nbsp;来自", "")

    sql = "INSERT INTO weibo_info VALUES ( '%s','%s','%s','%s','%s','%s','%s','%s','%s')" \
          % (weibo_id, weibo_content, "", weibo_zan_num, weibo_forward_num, weibo_comment_num, user_id,
             post_time, is_forward)
    MySQLClient.execute(sql)


def get_weibo_info(user_id):
    for i in range(5):
        page = i + 1
        user_url = "https://weibo.cn/%s/profile?page=%s" % (user_id, page)
        print "正在获取%s的第%s页微博列表" % (user_id, page)
        try:
            html = requests.get(user_url, headers=get_head())
            content = str(html.content)
            if len(content) == 0:
                print "微博反爬虫，等待1分钟"
                return None
            weibo_list = content.split('class="c" id')
            weibo_list.pop(0)

            if len(weibo_list) == 0:
                print "无法获取微博列表"
                return None

            for weibo_data in weibo_list:
                parse_weibo(weibo_data, user_id)

        except Exception, e:
            print e
            return None
    return "success"


def start_get_weibo_info():
    while True:
        user_id = MySQLClient.fetchone(
            "SELECT USER_ID FROM user_info u WHERE (SELECT COUNT(1) as num from weibo_info w WHERE u.USER_ID = w.POSTER_ID ) = 0 ")[
            0]
        if get_weibo_info(user_id) is None:
            time.sleep(30)
            change_cookie()
            continue
        print "%s的微博列表获取完成" % user_id


start_get_weibo_info()
