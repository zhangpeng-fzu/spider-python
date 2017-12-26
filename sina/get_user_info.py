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


def get_user_info(user_id):
    user_url = "https://weibo.cn/" + user_id
    try:
        html = requests.get(user_url, headers=head)
        content = str(html.content)
        results = re.findall(r"微博\[.*?\]", content, re.I | re.S | re.M)
        post_num = results[0].replace("微博[", "").replace("]", "")

        results = re.findall(r"粉丝\[.*?\]", content, re.I | re.S | re.M)
        fllower_num = results[0].replace("粉丝[", "").replace("]", "")

        results = re.findall(r"关注\[.*?\]", content, re.I | re.S | re.M)
        fllowee_num = results[0].replace("关注[", "").replace("]", "")

        results = re.findall(r"ut\">.*?<a", content, re.I | re.S | re.M)
        user_name = results[0].replace("ut\">", "").replace("<a", "").encode('UTF-8')

        sql = "INSERT INTO user_info VALUES ( '%s','%s','%s','%s','%s','%s') ON DUPLICATE KEY UPDATE USER_NAME = '%s',FLLOWER_NUM='%s',FLLOWEE_NUM='%s',POST_NUM='%s'" \
              % (user_id, user_name, user_url, fllower_num, fllowee_num, post_num, user_name, fllower_num, fllowee_num,
                 post_num)

        MySQLClient.execute(sql)

    except Exception, e:
        print e

while True:
    user_id = MySQLClient.fetchone("SELECT USER_ID FROM user_info WHERE USER_NAME is NULL ")[0]
    get_user_info("3166023711")
    count = MySQLClient.fetchone("select count(*) from user_info")[0]
    print user_id, count

