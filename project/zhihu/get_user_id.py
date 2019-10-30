# -*-coding:utf-8-*-

import sys
import time

import requests

from project import zhihu

connection = zhihu.init_connection()


# 获取关注列表 关注列表用户更有价值
def get_following(user_id):
    following_data = []
    page = 0

    # 分页获取列表
    while True:
        url = "https://www.zhihu.com/api/v4/members/" + user_id + "/followees?include=data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics&offset=" + str(
            page * 20) + "&limit=50"
        try:
            # 发起请求,得到响应结果
            r = requests.get(url, headers=zhihu.get_head())

            if r.status_code != 200:
                return r.status_code
            response_json = r.json()
            following_data = following_data + response_json["data"]
            page = page + 1

            # 一个用户最多只获取50页的关注列表
            if page > 50:
                break
            if len(response_json["data"]) < 20:
                break
        except Exception as e:
            print(e)

    if len(following_data) == 0:
        return 200

    # 关注者ID写入数据库，用户爬取用户详细数据
    for data in following_data:
        url_token = data["url_token"]
        try:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO user_info(ID) VALUES (%s)'
                cursor.execute(sql, url_token)
            connection.commit()
        except Exception as e:
            print(e)
    print("获取【%s】的关注列表完成，共%s条" % (user_id, len(following_data)))
    return 200


# 主程序
if __name__ == '__main__':
    try:
        while True:
            with connection.cursor() as cursor:

                # 查询当前已获取用户ID数量
                cursor.execute("select count(*) from user_info")
                ret = cursor.fetchall()
                count = int(ret[0]["count(*)"])

                # 当数量大于100000时停止爬取
                if count > zhihu.max_user_num:
                    print("已达到爬取用户最大数量，停止爬虫")
                    sys.exit()

                # 获取未被获取关注列表的用户ID
                cursor.execute("select ID from user_info WHERE FLAG = 0 limit 0,1")
                ret1 = cursor.fetchall()
                user_id = str(ret1[0]["ID"]).strip()

                try:
                    print("正在获取【%s】的关注列表" % user_id)
                    statu_code = get_following(user_id)
                    if statu_code != 200:
                        print("获取过程中出现异常，暂时停止抓取")
                        time.sleep(1)
                except Exception as e:
                    print(e)
                finally:
                    try:
                        # 更新记录，避免重复爬取
                        sql = 'UPDATE user_info set FLAG = 1 WHERE ID = %s'
                        cursor.execute(sql, user_id)
                        connection.commit()
                    except Exception as e:
                        print(e)
    except Exception as e:
        print(e)
    finally:
        connection.close()
