# -*-coding:utf-8-*-

import re
from mysql import MySQL
import requests
import time
import random

MySQLClient = MySQL()
MySQLClient.set_table("dianping")

head = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    "Host": "www.dianping.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.1.3282.186 Safari/537.31",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": 'navCtgScroll=54; s_ViewType=10; _lxsdk_cuid=161eef1ff9cc8-0608c2dd6957ab-32677b04-13c680-161eef1ff9dc8; _lxsdk=161eef1ff9cc8-0608c2dd6957ab-32677b04-13c680-161eef1ff9dc8; _hc.v=65bc51bb-00dc-a223-98c9-e47b965d62c4.1520132293; _lxsdk_s=161ef568b0e-651-63-3b2%7C%7C451'
}


# 请求大众点评商户主页
def get_shop_info(shop_id):
    print("正在获取【%s】的商铺信息" % shop_id)
    url = "http://www.dianping.com/shop/%s" % shop_id
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=head)
        if r.status_code != 200:
            return r.status_code
        response_text = str(r.content.decode())

        if "页面不存在" in response_text:
            return 403

        # 解析响应结果
        parseHtml(shop_id, response_text)
        return 200
    except Exception as e:
        print(e)


# 解析页面
def parseHtml(shop_id, response_text):
    results = re.findall(r"\"shop-name\".*?<", response_text, re.I | re.S | re.M)
    shop_name = ""
    if len(results) > 0:
        shop_name = results[0].replace("\"shop-name\">", "").replace("<", "").strip()

    address = ""
    results = re.findall(r"street-address\" title.*?>", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        address = results[0].replace("street-address\" title=\"", "").replace("\">", "").strip()

    phone = ""
    results = re.findall(r"itemprop=\"tel\">.*?<", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        phone = results[0].replace("itemprop=\"tel\">", "").replace("<", "").strip()

    taste_score = ""
    results = re.findall(r"口味:.*?<", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        taste_score = results[0].replace("口味:", "").replace("<", "").strip()

    env_score = ""
    results = re.findall(r"环境:.*?<", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        env_score = results[0].replace("环境:", "").replace("<", "").strip()

    service_score = ""
    results = re.findall(r"服务:.*?<", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        service_score = results[0].replace("服务:", "").replace("<", "").strip()

    avg_cost = ""
    results = re.findall(r"人均:.*?<", response_text, re.I | re.S | re.M)
    if len(results) > 0:
        avg_cost = results[0].replace("人均:", "").replace("<", "").strip()

    sql = 'UPDATE shop_info set SHOP_NAME = "%s",PHONE="%s",ADDRESS="%s",TASTE_SCORE="%s",ENV_SCORE="%s",SERVICE_SCORE="%s",AVG_COST="%s" WHERE ID="%s"' % \
          (shop_name, phone, address, taste_score, env_score, service_score, avg_cost, shop_id)
    try:
        MySQLClient.execute(sql)
    except Exception as e:
        print(e)


# 主程序
if __name__ == '__main__':
    while True:
        res = MySQLClient.fetchone('SELECT ID FROM shop_info WHERE shop_name is NULL limit 0,1')
        if res is None or len(res) == 0:
            print("暂时无新数据，请等待.....")
            time.sleep(10)

        shop_id = str(res[0])
        if shop_id is None or len(shop_id) == 0:
            break

        # 请求响应异常，可以由于网站反爬虫生效
        statu_code = get_shop_info(shop_id.strip())
        if statu_code != 200:
            print("触发网站反爬虫，更换useragent")
            head["User-Agent"] = head["User-Agent"] + str(random.randint(0, 10))

        # 休眠2s，调低抓取频率，避免触发反爬虫   备注：未休眠会很快触发反爬虫
        time.sleep(2)
