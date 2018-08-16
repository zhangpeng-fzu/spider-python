# _*_coding:utf-8_*_

import json
import time

import pymysql
import requests

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',  # 数据库密码
    'db': 'sina_news',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor,
}

connection = pymysql.connect(**config)

head = {
    "Accept": "*/*",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Content-Type": "charset=UTF-8",
    "Host": "api.roll.news.sina.com.cn",
    "Referer": "http://news.sina.com.cn/society/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    # 操作cookie
    "Cookie": 'aliyungf_tc=AQAAAGqNpwMtXAQAwwsjeC+Ws4nuRuQM; _xsrf=fe6774a0-913e-4dac-b949-e76a1304790c; q_c1=8008992a5439454d80034f17745e3f00|1519895601000|1519895601000; _zap=fede0ae4-2500-4aec-ad8c-d295c77b4d93; l_n_c=1; l_cap_id="ZjI2YTMxNGU4Y2IzNDRlODg3ODQ1MmI5MWVlODEwMDU=|1519895606|3d3793ae69f9f9e45336b100da5c7d29eae53b77"; r_cap_id="YzFkNzU5NjdmZDUzNDEzZTkwZjI0OGU1ZDNhZTgzM2Q=|1519895606|ede5d7f2d7a96c68ab48ced2147207d9156a722f"; cap_id="ZWQ4ODMyODA5OGQyNDUyZDhjMGNkYWJhYzY1ZThkOTc=|1519895606|ded435dd86c3ee222fd301b81e83187638bd761b"; n_c=1; d_c0="AADtA5W9Ow2PTiN6eigkl7Dt010OlHYhVrI=|1520127420"'
}


def get_news():
    print("开始抓取新闻列表")
    page = 0
    is_stop = False
    retry_times = 0

    # 分页获取列表
    while True and not is_stop:
        print("正在抓取第%s页的新闻" % page)
        url = "http://api.roll.news.sina.com.cn/zt_list?channel=news&cat_1=shxw&cat_2==zqsk||=qwys||=shwx||=fz-shyf&level==1||=2&show_ext=1&show_all=1&show_num=22&tag=1&format=json&page=%s&callback=newsloadercallback&_=1522463353503" % page
        try:
            # 发起请求,得到响应结果
            r = requests.get(url, headers=head)

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
                news_id = news["id"]
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
                              'VALUES (%s,%s,%s,%s,%s,%s) ' \
                              'ON DUPLICATE KEY UPDATE TITLE = %s,SOURCE = %s ,URL = %s,KEYWORDS = %s,CREATE_TIME=%s'
                        cursor.execute(sql, (
                            news_id, title, source, link, keywords, create_time, title, source, link, keywords,
                            create_time))
                    connection.commit()
                except Exception as e:
                    print("数据库写入失败", e)
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
            time.sleep(0.5)
