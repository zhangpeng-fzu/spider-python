# -*-coding:utf-8-*-

import configparser
import csv
import hashlib
import random
import re
import sys
import threading
import time
from v3 import zhenai
import requests
from threadpool import *

cf = configparser.ConfigParser()
cf.read("zhenai.ini", encoding="utf-8")

connection = zhenai.init_connection()

connection = pymysql.connect(**config)
MD5 = hashlib.md5()
lock = threading.RLock()

bucket = zhenai.init_bucket()

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

city_code_map = {}


# 通过关键词获取公司列表信息
def get_user_list(sex, begin_age, end_age, province, city, max_num):
    page = 1
    while True:

        if exceed_max_num(max_num):
            print("已达到最大用户爬取数量上限，结束爬虫！")
            break

        print("开始第%s页的用户数据！" % page)
        url = "http://search.zhenai.com/v2/search/getPinterestData.do?sex=%s&agebegin=%s&ageend=%s&workcityprovince=%s&workcitycity=%s&" \
              "h1=-1&h2=-1&salaryBegin=-1&salaryEnd=-1&occupation=-1&h=-1&c=-1&workcityprovince1=-1" \
              "&workcitycity1=-1&constellation=-1&animals=-1&stock=-1&belief=-1&condition=66&orderby=hpf&" \
              "hotIndex=0&online=&currentpage=%s&topSearch=true" % (sex, begin_age, end_age, province, city, page)
        try:

            r = requests.get(url, headers=head)

            if r.status_code != 200:
                print("第%s页的用户数据获取异常！code=%s" % r.status_code)
                break

            response_json = r.json()
            user_data = response_json["data"]

            if len(user_data) == 0:
                break

            for user in user_data:
                user["sex"] = sex
                user["cityCode"] = city_code

            my_requests = makeRequests(get_user_info_by_id, user_data)
            [pool.putRequest(req) for req in my_requests]
            pool.wait()
            print("第%s页的用户数据完成！" % page)

            page = page + 1
        except Exception as e:
            print(e)


def get_user_info_by_id(user):
    user_id = user["memberId"]
    city_code = user["cityCode"]
    sex = user["sex"]
    if not is_need_spider(user_id):
        print("【%s】的用户信息已存在，跳过" % user_id)
        return
    print("正在获取【%s】的用户信息" % user_id)

    nick_name = user["nickName"]
    age = str(user["age"]).replace("岁", "")
    photo_path = user["photopath"]

    photo_path = upload_file(photo_path)

    res = get_album(user_id)
    ablum = res["ablum"]
    if ablum is None or len(ablum) <= 1:
        print("【%s】的用户相册图片数量不大于1张，忽略该用户" % user_id)
        return

    introduce = res["introduce"]

    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = 'INSERT INTO user_info VALUES (%s, %s, %s, %s, %s, %s, %s,%s)'
            cursor.execute(sql, (user_id, nick_name, age, photo_path, sex, introduce, str(ablum), city_code))
            connection.commit()
    except Exception as e:
        print(e)
    print("完成获取【%s】的用户信息" % user_id)


# 判断是否需要抓取该用户
def is_need_spider(user_id):
    # lock.acquire()
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT ID FROM user_info WHERE ID=%s' % user_id
            cursor.execute(sql)
            res = cursor.fetchone()
            return res is None
    except Exception as e:
        print(e)
        return True
        # finally:
        # lock.release()


# 上传文件到阿里云
def upload_file(url):
    photo_stream = requests.get(url)

    file_dictory = "user_photos/" + time.strftime("%Y%m")
    MD5.update(((str(int(round(time.time() * 1000)))) + str(random.randint(0, 1000))).encode(encoding='utf-8'))
    file_name = MD5.hexdigest() + ".jpg"
    ali_file_path = file_dictory + "/" + file_name
    try:
        bucket.put_object(ali_file_path, photo_stream)
        return "http://xxroom.oss-cn-hangzhou.aliyuncs.com/" + ali_file_path
    except Exception as e:
        print(e)
        return url


# 获取相册和内心独白
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
        results = re.findall(r"data-mid-img.*?src", response_html, re.I | re.S | re.M)
        size = len(results)
        if size > 9:
            size = 9

        # 相册照片数量不大于1张，忽略该用户
        if size <= 1:
            return {"introduce": "", "ablum": ablum_list}

        for i in range(size):
            ablum_photo_url = upload_file(results[i].replace("data-mid-img=\"", "").replace("\" src", ""))
            ablum_list.append(ablum_photo_url)

        res = {"introduce": introduce.replace("&nbsp;", " ").replace("<br/>", "")[1:], "ablum": ablum_list}
        return res

    except Exception as e:
        print(e)
    time.sleep(0.1)


def exceed_max_num(max_num):
    try:
        with connection.cursor() as cursor:
            # 查询当前已获取用户ID数量
            cursor.execute("select count(*) from user_info")
            ret = cursor.fetchall()
            count = int(ret[0]["count(*)"])

            # 当数量大于设置上限时停止爬取
            if count > int(max_num):
                return True
    except Exception as e:
        print(e)
        return False


def init_code_map():
    csv_file = csv.reader(open("city.csv", encoding="utf-8"))
    for obj in csv_file:
        if len(obj) == 4:
            city_code = {"province": obj[2], "city": obj[3]}
            city_code_map[obj[0]] = city_code


# 主程序
if __name__ == '__main__':
    init_code_map()

    sex = cf.get("zhenai", "sex")
    city_code = cf.get("zhenai", "cityCode")
    max_num = cf.get("zhenai", "maxNum")
    begin_age = cf.get("zhenai", "beginAge")
    end_age = cf.get("zhenai", "endAge")
    province, city = "", ""
    try:
        province = city_code_map[city_code]["province"]
        city = city_code_map[city_code]["city"]
    except Exception as e:
        print(e)
        print("未找到该城市对应的code，请输入正确的城市编码")
        sys.exit()

    if city == "" or city is None:
        print("未找到该城市对应的code，请输入正确的城市编码")
        sys.exit()

    pool = ThreadPool(1)
    get_user_list(sex, begin_age, end_age, province, city, max_num)
