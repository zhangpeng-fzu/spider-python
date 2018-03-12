# -*-coding:utf-8-*-

import re
import time

import pymysql
import requests

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'db': 'zhenai',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)

# 获取公司请求的http头部数据
head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cookie": "CHANNEL=^~refererHost=www.baidu.com^~channelId=900122^~subid=^~; sid=cCGoIQcJs8PxbRuQaSMK; SEARCHWORD=3814649; Hm_lvt_2c8ad67df9e787ad29dbd54ee608f5d2=1520691159; login_health=fe93c3ba3c63f10594b56adb4673613719d45b2d1d196e69a3ac524446bef95004e4eea381888661cd01c3465fb6ef7489b2b251d2520b635fc83dcfb876a6e8; preLG_101705002=2018-03-09+16%3A22%3A22; isSignOut=%5E%7ElastLoginActionTime%3D1520691187303%5E%7E; p=%5E%7Eworkcity%3D10103008%5E%7Elh%3D101705002%5E%7Esex%3D0%5E%7Enickname%3DChris%5E%7Emt%3D1%5E%7Eage%3D27%5E%7Edby%3Dd6a56454a23ad82%5E%7E; mid=%5E%7Emid%3D101705002%5E%7E; loginactiontime=%5E%7Eloginactiontime%3D1520691187303%5E%7E; logininfo=%5E%7Elogininfo%3D18651607880%5E%7E; rmpwd=%5E%7Eloginmode%3D9%5E%7Elogininfo%3D18651607880%5E%7E; otherinfo=%5E%7Eisnew%3D1%5E%7E; hds=2; live800=%5E%7EisOfflineCity%3Dtrue%5E%7EinfoValue%3DuserId%253D101705002%2526name%253D101705002%2526memo%253D%5E%7E; ooo=%5E%7Esex%3D1%5E%7EworkCity%3D10103000%5E%7Eage2%3D28%5E%7Eage1%3D23%5E%7E; bottomRemind=%5E%7EisAuthGzt%3Dfalse%5E%7E; isvalideEmail=%5E%7EvalideEmail%3D0%5E%7E; dgpw=0; JSESSIONID=abcvz5ypGm92qfRkXqqiw; __xsptplusUT_14=1; __xsptplus14=14.2.1520864981.1520865048.7%234%7C%7C%7C%7C%7C%23%23cFBgPLJ21G2rvGB5tg3hik10JsnDPoEr%23; Hm_lpvt_2c8ad67df9e787ad29dbd54ee608f5d2=1520865049",
    "Host": "search.zhenai.com",
    "Origin": "https://www.lagou.com",
    "Referer": "http://search.zhenai.com/v2/search/pinterest.do?sex=1&agebegin=-1&ageend=-1&workcityprovince=10103000&workcitycity=-1&h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&hotIndex=0&online=",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


# 通过关键词获取公司列表信息
def get_user_info(sex):
    url = "http://search.zhenai.com/v2/search/getPinterestData.do?sex=%s&agebegin=18&ageend=-1&workcityprovince=10103000&workcitycity=-1&" \
          "h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1" \
          "&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&" \
          "hotIndex=0&online=&currentpage=1&topSearch=true" % sex
    try:
        r = requests.get(url, headers=head)
        response_json = r.json()
        user_data = response_json["data"]

        for user in user_data:
            user_id = user["memberId"]
            nickName = user["nickName"]
            age = str(user["age"]).replace("岁", "")
            photo_path = user["photopath"]

            res = get_album(user_id)
            ablum = res["ablum"]
            introduce = res["introduce"]

            if len(ablum) <= 1:
                continue

            try:
                with connection.cursor() as cursor:
                    # 执行sql语句，插入记录
                    sql = 'INSERT INTO user_info VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ' \
                          'NICK_NAME=%s,AGE=%s,PHOTO_PATH=%s,SEX=%s,INTRODUCE=%s,ALBUM=%s'
                    cursor.execute(sql, (
                        user_id, nickName, age, photo_path, sex, introduce, str(ablum),
                        nickName, age, photo_path, sex, introduce, str(ablum)))
                    connection.commit()
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


def get_album(member_id):
    url = "http://album.zhenai.com/u/%s" % member_id
    try:
        head["Host"] = "album.zhenai.com"
        head["Upgrade-Insecure-Requests"] = "1"
        r = requests.get(url, headers=head)
        response_html = str(r.content.decode("GBK"))

        introduce = ""
        results = re.findall(r"slider-area-js.*?span", response_html, re.I | re.S | re.M)
        if len(results) > 0:
            introduce = results[0].replace("lider-area-js\">", "").replace("<span", "")

        ablum_list = []
        results = re.findall(r"data-big-img.*?data-mid-img", response_html, re.I | re.S | re.M)
        size = len(results)
        if size > 9:
            size = 9
        for i in range(size):
            ablum_list.append(results[i].replace("data-big-img=\"", "").replace("\" data-mid-img", ""))

        res = {}
        res["introduce"] = introduce.replace("&nbsp;", " ").replace("<br/>", "")[1:]
        res["ablum"] = ablum_list
        return res

    except Exception as e:
        print(e)
        # 休息0.1s,防止触发网站反爬虫
    time.sleep(0.1)


# 主程序
if __name__ == '__main__':
    get_user_info(1)
