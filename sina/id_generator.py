# -*-coding:utf8-*-

import sys
import re
import requests
import time
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("weibo")

head = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_T_WM=95ca63e574bf94d74fc0c9b284d1d582; H5_INDEX_TITLE=%E8%BF%B7%E8%B7%AF%E5%85%88%E6%A3%AEMR; H5_INDEX=2; ALF=1516887822; SCF=AgZ3xgmGREeWkID4FJDNeBET7xC7a-N4i1y2RR-cI7XN7EOtAbpepmQyxtLHaKNybFNcjZpNTMK6NdsYNa2T6Ps.; SUB=_2A253RiXpDeRhGeVP7VQR8i3Lyj2IHXVUyUuhrDV6PUJbktBeLUjSkW1NTV9JKX5XD5Mbq2H2oGZqjoKTpYcikcZ1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh8NFjpvNEKOTAnQY.eSFS05JpX5K-hUgL.FoepSoq7eoeNeK22dJLoIEqLxKnLB.qLBoMLxKnLBoMLB-qLxK-L1h-L1hnLxKqLBKeLB-HS-ntt; SUHB=09PNE0WaSngpuC; SSOLoginState=1514296761',
    'Pragma': 'no-cache',
    'Referer': 'https://login.sina.com.cn/sso/login.php?url=https%3A%2F%2Fweibo.cn%2F3166023711%2Finfo&_rand=1514206231.9481&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.26',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Request': 'json',
    'X-Requested-With': 'XMLHttpRequest'
}


# 获取粉丝列表
# 由于微博智能反垃圾列表，会导致抓取的粉丝数少于显示数量
def get_fllower(user_id, page):
    print "正在获取%s的第%s页粉丝数据" % (user_id, page)
    user_url = "https://weibo.cn/%s/fans?page=%s" % (user_id, page)
    try:
        html = requests.get(user_url, headers=head)
        content = str(html.content)
        if len(content) == 0:
            print "获取粉丝列表失败"
            return None

        user_ids = re.findall(r"add\?uid=.*?&", content, re.I | re.S | re.M)
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
        html = requests.get(user_url, headers=head)
        content = str(html.content)

        if len(content) == 0:
            print "获取关注列表失败"
            return None

        user_ids = re.findall(r"add\?uid=.*?&", content, re.I | re.S | re.M)
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


user_id = "210576870"
count = 0
while user_id is not None and int(count) <= 15000:
    user_id = str(user_id)
    for i in range(20):
        if get_fllowee(user_id, i + 1) is None or get_fllower(user_id, i + 1) is None:
            time.sleep(600)

    MySQLClient.update("UPDATE user_info SET USER_NAME = ' ' WHERE USER_ID = '" + user_id + "'")
    user_id = MySQLClient.fetchone("SELECT USER_ID FROM user_info WHERE USER_NAME is NULL ")[0]
    count = MySQLClient.fetchone("select count(*) from user_info")[0]
    print user_id, count

# get_fllower("3166023711", 1)
