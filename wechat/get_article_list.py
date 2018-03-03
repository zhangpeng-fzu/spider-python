# -*-coding:utf8-*-

import sys
import re
import requests
import time
import json
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("article")

head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'rewardsn=; wxtokenkey=52363034789e417a147b34ee1592791c2faf0dbc3e17eab8c5c23f5d2fccdab5; wxuin=338385195; devicetype=Windows10; version=62060028; lang=zh_CN; pass_ticket=BzTu+TqcSTidBngcCpl/I1MyUnjkvwlJ9RXDEBD1b+k2ijuomwg/kE/s2Y+QUO5e; wap_sid2=CKuyraEBElx6eDdRQzBrTEVwQ2dpdGI2dFNQMXJ4X185WXMtTnB5a2NTenVtdmJsaHZ3d2ZzOFozaU9XdjJsOWJmNGJTcUNvbFlLVzVDNjdWWXd6N3Y5UnEtclZVYXNEQUFBfjCSivbSBTgNQJVO',
    'Pragma': 'no-cache',
    'Referer': 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MjM5NjA4NzUwNw==&scene=123&uin=MzM4Mzg1MTk1&key=a5093a3f4494c6b19f6e56165af5e5625076f5a6ac48e36474027d512210395610ea2b2e65ec43c246d905fba8054e628cd34e23819baa2b177e818db6d9a3bf4d0f791b67f964bc17d47e4763ec30e4&devicetype=Windows+10&version=62060028&lang=zh_CN&a8scene=1&pass_ticket=BzTu%2BTqcSTidBngcCpl%2FI1MyUnjkvwlJ9RXDEBD1b%2Bk2ijuomwg%2FkE%2Fs2Y%2BQUO5e&winzoom=1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
    'X-Requested-With': 'XMLHttpRequest',
    'Host': 'mp.weixin.qq.com'
}


def get_article_list(page):
    page = page - 1
    offset = page * 10
    user_url = "https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MjM5NjA4NzUwNw==&f=json&offset=" + str(
        offset) + "&count=10&is_ok=1&scene=123&uin=MzM4Mzg1MTk1&key=a5093a3f4494c6b19f6e56165af5e5625076f5a6ac48e36474027d512210395610ea2b2e65ec43c246d905fba8054e628cd34e23819baa2b177e818db6d9a3bf4d0f791b67f964bc17d47e4763ec30e4&pass_ticket=BzTu%2BTqcSTidBngcCpl%2FI1MyUnjkvwlJ9RXDEBD1b%2Bk2ijuomwg%2FkE%2Fs2Y%2BQUO5e&wxtoken&appmsg_token=939_fREbmAFlNVsYzA%252BM6-8jmuHDXZ3WNVj73VfTiA~~&x5=0&f=json"

    r = requests.get(user_url, headers=head)
    articles_list = json.loads(r.json()["general_msg_list"])["list"]

    if len(articles_list) == 0:
        return 0

    for i in range(len(articles_list)):
        try:
            article = articles_list[i]
            aid = article["comm_msg_info"]["id"]
            create_time_local = time.localtime(article["comm_msg_info"]["datetime"])
            create_time = time.strftime("%Y-%m-%d", create_time_local)
            title = article["app_msg_ext_info"]["title"]
            author = article["app_msg_ext_info"]["author"]
            sql = "INSERT INTO article VALUES ( '%s','%s','%s','%s') ON DUPLICATE KEY UPDATE TITLE = '%s',AUTHOR = '%s',CREATE_TIME='%s'" % (
                aid, title, author, create_time, title, author, create_time)
            MySQLClient.execute(sql)
        except Exception, e:
            print e
    return 1


i = 1
while True:
    print "正在获取第%s页文章列表" % i
    if get_article_list(i) == 0:
        break
    print "获取第%s页文章列表完成" % i
    i = i + 1
print "获取文章列表完成"
