# -*-coding:utf-8-*-

import json
import re
import time

import requests

from v3 import zhihu

connection = zhihu.init_connection()


# 请求知乎用户主页
def get_user_info(user_id):
    print("正在获取【%s】的用户信息" % user_id)
    url = "https://www.zhihu.com/people/%s/activities" % user_id
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=zhihu.get_head())
        if r.status_code != 200:
            return r.status_code

        # 数据解析失败
        response_text = str(r.content.decode())
        if not parseHtml(user_id, response_text):
            return 400

        return 200

    except Exception as e:
        print(e)
        return 400


# 解析页面
def parseHtml(user_id, response_text):
    userd_data_str = ""
    results = re.findall(r"data-state.*?data-config", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        userd_data_str = results[0].replace("data-state=\"", "").replace("\" data-config", "").replace("&quot;", "\"")

    results = re.findall(r"users.*?questions", userd_data_str, re.I | re.S | re.M)
    if len(results) > 0:
        userd_data_str = results[0].replace("users\":", "").replace(",\"questions", "")

    # 处理数据 避免json反序列化失败
    regex = re.compile(r'\\(?![/u"])')
    fixed = regex.sub(r"\\\\", userd_data_str)

    # 获取用户json数据 当数据为空时 可能是用户被禁或者反爬虫
    try:
        userd_data_json = json.loads(fixed)[user_id]
    except Exception as e:
        return False

    # 性别 0:女 1:男 -1:不男不女
    genger = userd_data_json["gender"]

    # 用户地理位置
    try:
        if len(userd_data_json["locations"]) > 0:
            location = userd_data_json["locations"][0]["name"]
        else:
            location = str(userd_data_json["locations"])
    except Exception as e:
        location = "[]"
    # 赞同数
    voteupCount = userd_data_json["voteupCount"]
    # 感谢数
    thankedCount = userd_data_json["thankedCount"]
    # 关注数
    followingCount = userd_data_json["followingCount"]
    # 被关注数
    followerCount = userd_data_json["followerCount"]

    # 收藏数
    favoriteCount = userd_data_json["favoriteCount"]
    # 回答数
    answerCount = userd_data_json["answerCount"]
    # 文章数
    articlesCount = userd_data_json["articlesCount"]
    # 提问数
    pinsCount = userd_data_json["pinsCount"]

    # 学历信息
    try:
        if len(userd_data_json["locations"]) > 0:
            educations = userd_data_json["educations"][0]["school"]["name"]
        else:
            educations = str(userd_data_json["educations"])
    except Exception as e:
        educations = "[]"
    try:
        if len(userd_data_json["employments"]) > 0:
            # 公司
            company = userd_data_json["employments"][0]["company"]["name"]
            # 职位
            job = userd_data_json["employments"][0]["job"]["name"]
        else:
            company, job = "", ""
    except Exception as e:
        company, job = "", ""

    # 行业
    try:
        if userd_data_json["business"]:
            business = userd_data_json["business"]["name"]
        else:
            business = ""
    except Exception as e:
        business = ""

    try:
        with connection.cursor() as cursor:
            # 执行sql语句，插入记录
            sql = 'INSERT INTO user_info VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s) ON DUPLICATE KEY UPDATE ' \
                  'GENDER=%s,VOTEUP_COUNT=%s,THANKED_COUNT=%s,FOLLOWING_COUNT=%s,FOLLOWER_COUNT=%s,FAVORITE_COUNT=%s,ANSWER_COUNT=%s,ARTICLES_COUNT=%s,PINS_COUNT=%s,LOCATION=%s,' \
                  'EDUCATION=%s,COMPANY=%s,JOB=%s,BUSINESS=%s'
            cursor.execute(sql, (
                user_id, genger, voteupCount, thankedCount, followingCount, followerCount, favoriteCount, answerCount,
                articlesCount, pinsCount, location, educations, company, job, business, 0,
                genger, voteupCount, thankedCount, followingCount, followerCount, favoriteCount,
                answerCount,
                articlesCount, pinsCount, location, educations,
                company,
                job,
                business))
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return True


# 主程序
if __name__ == '__main__':
    try:
        # pool = ThreadPool(5)

        while True:
            with connection.cursor() as cursor:
                cursor.execute("select ID from user_info WHERE LOCATION is NULL limit 0,1")
                ret1 = cursor.fetchall()

                # 线程池处理，很容易触发反爬虫，慎用
                # ids = []
                # for dic in ret1:
                #     ids.append(str(dic["ID"]).strip())
                #
                # my_requests = makeRequests(get_user_info, ids)
                # [pool.putRequest(req) for req in my_requests]
                # pool.wait()

                user_id = str(ret1[0]["ID"]).strip()
                # if get_user_info("xu-chen-hao-9-24") != 200:
                if get_user_info(user_id) != 200:
                    print("获取用户信息出现异常，暂时停止爬虫")
                    try:
                        cursor.execute('UPDATE user_info set LOCATION = "invalid" WHERE ID = %s', user_id)
                        connection.commit()
                    except Exception as e:
                        print(e)

                    time.sleep(1)
                time.sleep(0.5)
    except Exception as e:
        print(e)
    finally:
        connection.close()
