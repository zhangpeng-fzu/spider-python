# _*_coding:utf-8_*_

import json
import random
import re
import string

import requests
from threadpool import *

head = {
    "Accept":
    "*/*",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language":
    "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection":
    "keep-alive",
    "Cache-Control":
    "max-age=0",
    "Content-Type":
    "charset=UTF-8",
    "Host":
    "api.roll.news.sina.com.cn",
    # "Referer": "http://news.sina.com.cn/society/",
    "User-Agent":
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    # 操作cookie
    "Cookie":
    'uuid=6757f1488e1901591a9.1530011152.1.0.0; _lxsdk_cuid=1643bc56fffc8-0c54e05fa94071-7c153a4a-1fa400-1643bc56fffc8; __mta=51256854.1530011152530.1530011152530.1530011153891.2; _lxsdk_s=1643bc57000-214-9db-a24%7C%7C4'
}
host = "hf.meituan.com"

old_phone_list = []
new_phone_list = []

flag = 6757


def load_phone():
    f = open("phohe.txt", "r")
    for line in f.readlines():
        if len(line) > 0 and line.replace("\n", "") not in old_phone_list:
            old_phone_list.append(line.replace("\n", ""))
    f.close()


def get_phone_by_Id(shop_id):
    global flag
    url = "http://%s/jiankangliren/%s/" % (host, shop_id)
    phone = None
    try:
        # 发起请求,得到响应结果
        head["Host"] = host
        r = requests.get(url, headers=head)

        if r.status_code != 200:
            new_flag = random.randint(0, 999999)
            head["Cookie"] = head["Cookie"].replace(str(flag), str(new_flag))
            flag = new_flag

        response_content = r.content.decode('utf-8')
        results = re.findall(r"电话：</span><span>.*?</span>", response_content,
                             re.I | re.S | re.M)

        if len(results) > 0:
            phone = results[0].replace("电话：</span><span>", "").replace(
                "</span>", "")
        if phone is None:
            return
        if phone in old_phone_list:
            print("号码【%s】已存在，跳过" % phone)
            return
        if "/" in phone:
            phone_arr = phone.split("/")
            if len(phone_arr[0]) == 11 and "-" not in phone_arr[
                    0] and phone_arr[0] not in old_phone_list:
                new_phone_list.append(phone_arr[0])
                print("获取新号码【%s】" % phone_arr[0])
            if len(phone_arr[1]) == 11 and "-" not in phone_arr[
                    1] and phone_arr[1] not in old_phone_list:
                new_phone_list.append(phone_arr[1])
                print("获取新号码【%s】" % phone_arr[1])
        else:
            if len(phone) == 11 and "-" not in phone:
                new_phone_list.append(phone)
                print("获取新号码【%s】" % phone)
    except Exception as e:
        print("获取手机号码异常!", e)


def get_phone_list():
    print("开始抓取商铺手机号码")
    global flag
    page = 1
    is_stop = False
    retry_times = 0
    total = len(old_phone_list)
    # 分页获取列表
    while not is_stop and total <= 50000:
        print("正在抓取第%s页的商铺信息" % page)
        url = "http://%s/jiankangliren/c74/pn%s/" % (host, page)
        try:
            # 发起请求,得到响应结果
            head["Host"] = host
            r = requests.get(url, headers=head)

            if r.status_code != 200:
                new_flag = random.randint(0, 999999)
                head["Cookie"] = head["Cookie"].replace(
                    str(flag), str(new_flag))
                flag = new_flag
                retry_times = retry_times + 1
                if retry_times <= 3:
                    print(
                        "获取列表异常，第%s次重试!code=%s" % (retry_times, r.status_code))
                else:
                    print("获取列表异常，终止爬虫!code=%s", r.status_code)
                    is_stop = True
                continue

            response_content = r.content.decode('utf-8')
            results = re.findall(r"<script>window.AppData.*?</script>",
                                 response_content, re.I | re.S | re.M)
            content = ""
            if len(results) > 0:
                content = results[0].replace("<script>window.AppData = ",
                                             "").replace(";</script>", "")
            response_list = json.loads(content)
            try:
                search_result = response_list["searchResult"]["searchResult"]
            except:
                print("触发反爬虫，更换cookie")
                new_flag = random.randint(0, 999999)
                head["Cookie"] = head["Cookie"].replace(
                    str(flag), str(new_flag))
                flag = new_flag
                continue
            if len(search_result) == 0:
                print("该城市已全部爬取完成")
                return new_phone_list
            ids = []
            for result in search_result:
                search_id = result["id"]
                ids.append(search_id)
            my_requests = makeRequests(get_phone_by_Id, ids)
            [pool.putRequest(req) for req in my_requests]
            pool.wait()
            # phone = get_phone_by_Id(search_id)
            total = len(old_phone_list) + len(new_phone_list)
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
                is_stop = True
    return new_phone_list


if __name__ == '__main__':
    load_phone()

    # cities = ["dl",
    #           "fs", "hk", "jn", "gz", "nc", "ly", "sjz", "sy", "gl", "km", "lyg", "ks", "nb", "nd", "np", "lz", "sy",
    #           "st", "ty", "yz", "zj", "zs", "cc"]
    pool = ThreadPool(10)
    # for city in cities:
    for i in string.ascii_lowercase:
        for j in string.ascii_lowercase:
            if i == "a" or i == "b" or i == "c" or i == "d":
                continue
            city = i + j
            print("city=" + city)

            host = city + ".meituan.com"
            phone_list = list(set(get_phone_list()))
            print("%s的数据已经爬取完成" % city)
            f = open("phohe.txt", "a+")
            for phone in phone_list:
                if len(
                        phone
                ) == 11 and "-" not in phone and phone not in old_phone_list:
                    f.write(phone + "\n")
                    old_phone_list.append(phone)
            f.close()
