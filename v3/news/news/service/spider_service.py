# _*_coding:utf-8_*_

import collections
import json
import time
import requests
from ..config import constants
import random


def request_list(url, source):
    retry_times = 0
    try:
        while retry_times < 3:
            # 发起请求,得到响应结果
            r = requests.get(url, headers=constants.headers[source])

            if r.status_code != 200:
                retry_times = retry_times + 1
                if retry_times <= 3:
                    print("获取列表异常，第%s次重试!code=%s" % (retry_times, r.status_code))
                    continue
                else:
                    print("获取列表异常，终止爬虫!code=%s", r.status_code)
                    return None
            return r.content
    except Exception as e:
        retry_times = retry_times + 1
        if retry_times <= 3:
            print(e)
            print("获取列表异常，第%s次重试!" % retry_times)
        else:
            print("获取列表异常，终止爬虫!code=%s", e)
            return None
    finally:
        time.sleep(0.2)


def spide_sina():
    print("开始抓取新浪新闻列表")

    retry_times = 0
    page = 1
    while not constants.isStop:
        url = "https://feed.sina.com.cn/api/roll/get?pageid=121&lid=1356&num=20&versionNumber=1.2.4&page=%s&encode=utf-8&callback=feedCardJsonpCallback&_=1556084987465" % page
        try:
            response = request_list(url, "sina")
            if response is None:
                constants.isStop = True
                break

            response_content = response.decode('utf-8').replace("try{", "").replace("}catch(e){};", "").replace(
                "feedCardJsonpCallback(", "").replace(");", "")
            response_list = json.loads(response_content)
            if len(response_list) == 0:
                print("数据爬取完成，结束爬虫")
                constants.isStop = True
                break

            for news in response_list["result"]["data"]:
                news_id = str(news["oid"])
                title = news["title"]
                keywords = news["keywords"]
                source = news["media_name"]
                timestamp = int(news["ctime"])
                if timestamp < 1325347200:
                    print("数据爬取完成，结束爬虫!timestamp=" + str(timestamp))
                    constants.isStop = True
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
                        connection.commit()
                except Exception as e:
                    print("数据库写入失败,停止抓取", e)
                    if str(flag) == "0":
                        constants.isStop = True
                        break
            if page % 10 == 0:
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
                constants.isStop = True
        finally:
            time.sleep(0.2)
    print("获取新浪数据结束")


def spider(flag, source):
    if str(flag) == "1":
        deleteAll()

    if source == 'sina':
        spide_sina()
    elif source == "tx":
        spider_tx()
    else:
        spider_netease()


def spider_tx():
    print("开始抓取腾讯新闻列表")

    retry_times = 0
    page = 1
    while not constants.isStop:
        url = "https://pacaio.match.qq.com/irs/rcd?cid=137&token=d0f13d594edfc180f5bf6b845456f3ea&id=&ext=top&page=%s&expIds=20190424008302|20190424A0BD7E|20190424A0CZL6|20190424008479|20190424A07XYG|20190424A09F72|20190421002547|20190424A09RFU|20190424A0CT9S|20190423006015&callback=__jp4" % page
        try:
            response = request_list(url, "tx")
            if response is None:
                constants.isStop = True
                break

            response_content = response.decode('utf-8').replace("__jp4(", "").replace(")", "")
            response_list = json.loads(response_content)
            if len(response_list) == 0:
                print("数据爬取完成，结束爬虫")
                constants.isStop = True
                break

            for news in response_list["data"]:
                news_id = str(news["id"])
                title = news["title"]
                keywords = news["keywords"]
                source = news["source"]
                create_time = news["publish_time"]

                link = news["url"]
                try:
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO news(ID,TITLE,SOURCE,URL,KEYWORDS,CREATE_TIME) ' \
                              'VALUES (%s,%s,%s,%s,%s,%s)'
                        cursor.execute(sql, (
                            news_id, title, source, link, keywords, create_time))
                        connection.commit()
                except Exception as e:
                    print("数据库写入失败,停止抓取", e)
                    if str(flag) == "0":
                        constants.isStop = True
                        break
            if page % 10 == 0:
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
                constants.isStop = True
        finally:
            time.sleep(0.2)
    print("获取数据结束")


def spider_netease():
    print("开始抓取网易新闻列表")

    retry_times = 0
    page = 1
    while not constants.isStop:
        if page == 1:
            url = "https://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback"
        else:
            url = "https://temp.163.com/special/00804KVA/cm_guonei.js_0%s?callback=data_callback" % page
        try:
            response = request_list(url, "netease")
            if response is None:
                constants.isStop = True
                break

            response_content = response.decode('gbk').replace("\n", "").replace("data_callback(", "").replace(")", "").strip()
            response_list = json.loads(response_content)
            if len(response_list) == 0:
                print("数据爬取完成，结束爬虫")
                constants.isStop = True
                break

            for news in response_list:
                news_id = "nt_" + str(random.choice(range(10000000)))
                title = news["title"]

                keywordsArr = news["keywords"]
                keywords = ""
                for keyword in keywordsArr:
                    keywords = keywords + keyword["keyname"] + ","
                source = news["channelname"]
                create_time = news["time"]

                link = news["tlink"]
                try:
                    with connection.cursor() as cursor:
                        sql = 'INSERT INTO news(ID,TITLE,SOURCE,URL,KEYWORDS,CREATE_TIME) ' \
                              'VALUES (%s,%s,%s,%s,%s,%s)'
                        cursor.execute(sql, (
                            news_id, title, source, link, keywords, create_time))
                        connection.commit()
                except Exception as e:
                    print("数据库写入失败,停止抓取", e)
                    if str(flag) == "0":
                        constants.isStop = True
                        break
            if page % 10 == 0:
                print("抓取第%s页的新闻完成" % page)
            retry_times = 0
            page = page + 1
        except Exception as e:
            retry_times = retry_times + 1
            if retry_times <= 3:
                print(e)
                print("获取列表异常，第%s次重试!" % retry_times)
                continue
            else:
                print("获取列表异常，终止爬虫!")
                constants.isStop = True
        finally:
            time.sleep(0.2)
    print("获取数据结束")
