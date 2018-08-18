# _*_coding:utf-8_*_

import collections
import json
import time

import config
import db
import requests

connection = db.get_connection()
headers = config.headers


def spider(flag):
    print("开始抓取新闻列表")
    page = 1
    is_stop = False
    retry_times = 0

    if str(flag) == "1":
        deleteAll()
    # 分页获取列表
    while True and not is_stop and not config.isStop:
        print("正在抓取第%s页的新闻" % page)
        url = "http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=shxw&cat_2==zqsk||=qwys||=shwx||=fz-shyf&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=%s&callback=newsloadercallback&_=1522463353503" % page
        try:
            # 发起请求,得到响应结果
            r = requests.get(url, headers=headers)

            if r.status_code != 200:
                retry_times = retry_times + 1
                if retry_times <= 3:
                    print("获取列表异常，第%s次重试!code=%s" % (retry_times, r.status_code))
                else:
                    print("获取列表异常，终止爬虫!code=%s", r.status_code)
                    is_stop = True
                continue

            response_content = r.content.decode('utf-8').replace("newsloadercallback(", "").replace(");", "")
            response_list = json.loads(response_content)
            if len(response_list) == 0:
                print("数据爬取完成，结束爬虫")
                is_stop = True
                break

            for news in response_list["result"]["data"]:
                news_id = str(news["id"]).replace("-", "")
                title = news["title"]
                keywords = news["keywords"]
                source = news["media_name"]
                timestamp = int(news["createtime"])
                if timestamp < 1325347200:
                    print("数据爬取完成，结束爬虫!timestamp=" + str(timestamp))
                    is_stop = True
                    break

                time_local = time.localtime(timestamp)
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                link = news["url"]
                try:
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO news(ID,TITLE,SOURCE,URL,KEYWORDS,CREATE_TIME) ' \
                              'VALUES (%s,%s,%s,%s,%s,%s)'
                        cursor.execute(sql, (
                            news_id, title, source, link, keywords, create_time))
                except Exception as e:
                    print("数据库写入失败,停止抓取", e)
                    is_stop = True
                    break

            print("抓取第%s页的新闻完成" % page)
            retry_times = 0
            page = page + 1
        except Exception as e:
            retry_times = retry_times + 1
            if retry_times <= 3:
                print(e)
                print("获取列表异常，第%s次重试!code=%s" % (retry_times, r.status_code))
                continue
            else:
                print("获取列表异常，终止爬虫!code=%s", r.status_code)
                is_stop = True
        finally:
            time.sleep(0.2)


def get_list():
    try:
        with connection.cursor() as cursor:
            sql = 'SELECT * from news'
            cursor.execute(sql)
            rows = cursor.fetchall()  # 获取查询的所有记录
            result = {}
            # 遍历结果
            objects_list = []
            for row in rows:
                d = collections.OrderedDict()
                d['id'] = row["ID"]
                d['title'] = row["TITLE"]
                d['source'] = row["SOURCE"]
                d['url'] = row["URL"]
                d['keywords'] = row["KEYWORDS"]
                d['createTime'] = str(row["CREATE_TIME"])
                objects_list.append(d)
            result["data"] = objects_list
            return json.dumps(result)

    except Exception as e:
        print("数据库获取列表失败", e)


def deleteAll():
    try:
        with connection.cursor() as cursor:
            sql = 'truncate news'
            cursor.execute(sql)

    except Exception as e:
        print("数据库获取列表失败", e)


def deleteOne(newsId):
    try:
        with connection.cursor() as cursor:
            sql = "delete from news WHERE ID = '" + newsId + "'"
            cursor.execute(sql)

    except Exception as e:
        print("数据库获取列表失败", e)


if __name__ == '__main__':
    spider(1)
