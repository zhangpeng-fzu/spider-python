# -*-coding:utf-8-*-

import re
from mysql import MySQL
import requests
import time

MySQLClient = MySQL()
MySQLClient.set_table("dianping")

head = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "no-cache",
    # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "www.dianping.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    "Cookie": 'navCtgScroll=54; s_ViewType=10; _lxsdk_cuid=161eef1ff9cc8-0608c2dd6957ab-32677b04-13c680-161eef1ff9dc8; _lxsdk=161eef1ff9cc8-0608c2dd6957ab-32677b04-13c680-161eef1ff9dc8; _hc.v=65bc51bb-00dc-a223-98c9-e47b965d62c4.1520132293; _lxsdk_s=161ef568b0e-651-63-3b2%7C%7C451'
}
type_code = {

    "苏州江浙": "g101",
    "自助餐": "g111",
    "面包甜点": "g117",
    "火锅": "g110",
    "咖啡厅": "g132",
    "酒吧": "g133",
    "韩国料理": "g114",
    "日本菜": "g113",
    "粤菜": "g103",
    "西餐": "g116",
    "小吃快餐": "g112",
    "烧烤": "g508",
    "东南亚菜": "g115",
    "面馆": "g215",
    "下午茶": "g34014",
    "川菜": "g102",
    "海鲜": "g251",
    "茶馆": "g134",
    "创意菜": "g250",
    "湘菜": "g104",
    "小龙虾": "g219",
    "私房菜": "g1338",
    "其他美食": "g118",
    "水果生鲜": "g2714",
    "早茶": "g34055"

}


# 请求大众电脑商户列表
def get_shop_list(code):
    page = 1
    while True:
        print "正在获取【%s】第%s页的商铺信息" % (code, page)
        url = "http://www.dianping.com/suzhou/ch10/%sr1699p%s" % (type_code[code], page)
        try:
            # 发起请求,得到响应结果
            r = requests.get(url, headers=head)
            if r.status_code != 200:
                return r.status_code
            response_text = str(r.content.decode())

            if "页面不存在" in response_text:
                print "触发网站反爬虫，更换cookie"
                break
            num = parseHtml(response_text.replace("\n", "").replace(' ', ''))

            print "完成获取【%s】第%s页的商铺信息,共%s条" % (code, page, num)
            page = page + 1
            time.sleep(1)
            if num < 15:
                break
        except Exception as e:
            print(e)


def parseHtml(response_text):
    results = re.findall(r"shopIDs.*?\]", response_text, re.I | re.S | re.M)
    ids = []
    if len(results) > 0:
        ids = results[0].replace("shopIDs:[", "").replace("]", "").split(",")
        ids.pop()

    # 未获取到ID
    if len(ids) == 0:
        return 0
    results = re.findall(r"recommend-click.*?<", response_text, re.I | re.S | re.M)

    # 获取推荐菜品链接
    recommend_list = []
    if len(results) > 0:
        for result in results:
            recommend_list.append(result.split("href=\"")[1].split("\"data-click-name")[0])
    for shop_id in ids:
        recommend = ""
        for recommend_url in recommend_list:
            if shop_id in recommend_url:
                recommend = recommend + get_recommend_info(recommend_url) + " "

        # ID记录数据库
        if len(shop_id) > 0:
            sql = 'INSERT INTO shop_info(ID,RECOMMEND) VALUES("%s","%s") ON DUPLICATE KEY UPDATE RECOMMEND="%s"' % (
                shop_id, recommend, recommend)
            MySQLClient.execute(sql)
    return len(ids)


# 获取推荐菜品及推荐次数
def get_recommend_info(url):
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=head)
        if r.status_code != 200:
            return r.status_code
        response_text = str(r.content.decode())
        results = re.findall(r"dish-name\">.*?<", response_text, re.I | re.S | re.M)
        dish_name = ""
        if len(results) > 0:
            dish_name = results[0].replace("dish-name\">", "").replace("<", "").strip()

        num = "0"
        results = re.findall(r"people-num\">.*?<", response_text, re.I | re.S | re.M)
        if len(results) > 0:
            num = results[0].replace("people-num\">", "").replace("<", "").strip()
        return dish_name + ":" + num

    except Exception as e:
        print(e)


# 主程序
if __name__ == '__main__':
    for code in type_code.keys():
        get_shop_list(code)
