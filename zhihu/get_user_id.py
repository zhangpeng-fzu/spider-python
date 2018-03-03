# -*-coding:utf-8-*-

import time
import zhihu
import pymysql.cursors
import requests

config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',
    'db': 'zhihu',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

# Connect to the database
connection = pymysql.connect(**config)


def get_following(user_id):
    url = "https://www.zhihu.com/api/v4/members/" + user_id + "/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=0&limit=50"
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=zhihu.get_head())

        if r.status_code != 200:
            return r.status_code
        response_json = r.json()
        following_data = response_json["data"]

        if len(following_data) == 0:
            return 200

        for data in following_data:
            url_token = data["url_token"]
            try:
                with connection.cursor() as cursor:
                    # 执行sql语句，插入记录
                    sql = 'INSERT INTO user_info(ID) VALUES (%s)'
                    cursor.execute(sql, url_token)
                # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
                connection.commit()
            except Exception as e:
                print(e)
        print("获取【%s】的关注列表完成，共%s条" % (user_id, len(following_data)))
        return 200
    except Exception as e:
        print(e)
    finally:
        try:
            with connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'UPDATE user_info set FLAG = 1 WHERE ID = %s'
                cursor.execute(sql, user_id)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            connection.commit()
        except Exception as e:
            print(e)


# 主程序
if __name__ == '__main__':
    try:

        while True:

            with connection.cursor() as cursor:
                sql = "select count(*) from user_info"
                cursor.execute(sql)
                ret = cursor.fetchall()
                count = int(ret[0]["count(*)"])

                if count < 100000:
                    sql = "select ID from user_info WHERE FLAG = 0 limit 0,1"
                    cursor.execute(sql)
                    ret1 = cursor.fetchall()
                    user_id = str(ret1[0]["ID"]).strip()
                    print("正在获取【%s】的关注列表" % user_id)
                    statu_code = get_following(user_id)
                    if statu_code != 200:
                        print("获取过程中出现异常，暂时停止抓取")
                        time.sleep(10)
                time.sleep(1)
    except Exception as e:
        print(e)
    finally:
        connection.close()
