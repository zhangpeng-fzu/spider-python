# -*-coding:utf8-*-

import sys
import re
import requests
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
    'Cookie': 'ALF=1516798146; SCF=AgZ3xgmGREeWkID4FJDNeBET7xC7a-N4i1y2RR-cI7XNt93Kiqq-aIhchAoXCTFWwKB5Z0DlRMPcb3jifKmYY_s.; SUB=_2A253RIRIDeRhGeVP7VQR8i3Lyj2IHXVUxiwArDV6PUJbktBeLUn5kW1NTV9JKUQF6Khr5mjr-JLCf1f2RWyPHXd8; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Wh8NFjpvNEKOTAnQY.eSFS05JpX5K-hUgL.FoepSoq7eoeNeK22dJLoIEqLxKnLB.qLBoMLxKnLBoMLB-qLxK-L1h-L1hnLxKqLBKeLB-HS-ntt; SUHB=04WejdjaI6MWGc; SSOLoginState=1514206233; _T_WM=95ca63e574bf94d74fc0c9b284d1d582',
    'Host': 'weibo.cn',
    'Pragma': 'no-cache',
    'Referer': 'https://login.sina.com.cn/sso/login.php?url=https%3A%2F%2Fweibo.cn%2F3166023711%2Finfo&_rand=1514206231.9481&gateway=1&service=sinawap&entry=sinawap&useticket=1&returntype=META&sudaref=&_client_version=0.6.26',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Request': 'json',
    'X-Requested-With': 'XMLHttpRequest'
}


# 获取粉丝列表
# 由于微博智能反垃圾列表，会导致抓取的粉丝数少于显示数量
def get_fllower(user_id, page):
    print "正在获取第%s页粉丝数据" % page
    user_url = "https://weibo.cn/%s/fans?page=%s" % (user_id, page)
    try:
        html = requests.get(user_url, headers=head)
        content = str(html.content)

        user_ids = re.findall(r"remove\?uid=.*?&", content, re.I | re.S | re.M)
        for fllower_id in user_ids:
            sql = "INSERT INTO fllower VALUES ('%s','%s')" % (
                user_id, fllower_id.replace("remove?uid=", "").replace("&", ""))
            MySQLClient.execute(sql)

        if page == 1:
            results = re.findall(r"粉丝\[.*?\]", content, re.I | re.S | re.M)
            fllower_num = results[0].replace("粉丝[", "").replace("]", "")
            pages = int(fllower_num) / 10

            for i in range(pages):
                get_fllower(user_id, i + 2)

    except Exception, e:
        print e


# 获取关注列表
# 由于微博智能反垃圾列表，会导致抓取的粉丝数少于显示数量
def get_fllowee(user_id, page):
    print "正在获取第%s页关注数据" % page
    user_url = "https://weibo.cn/%s/follow?page=%s" % (user_id, page)
    try:
        html = requests.get(user_url, headers=head)
        content = str(html.content)

        user_ids = re.findall(r"chat\?uid=.*?&", content, re.I | re.S | re.M)
        for fllowee_id in user_ids:
            sql = "INSERT INTO fllowee VALUES ('%s','%s')" % (
                user_id, fllowee_id.replace("chat?uid=", "").replace("&", ""))
            MySQLClient.execute(sql)

        if page == 1:
            results = re.findall(r"关注\[.*?\]", content, re.I | re.S | re.M)
            fllower_num = results[0].replace("关注[", "").replace("]", "")
            pages = int(fllower_num) / 10

            for i in range(pages):
                get_fllowee(user_id, i + 2)

    except Exception, e:
        print e


get_fllowee("3166023711", 1)
# get_fllower("3166023711", 1)
