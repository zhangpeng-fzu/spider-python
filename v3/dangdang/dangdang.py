# _*_coding:utf-8_*_

import json
import re

import pymysql
import requests

# 数据库配置
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'admin',  # 数据库密码
    'db': 'dangdang',
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
    "Host": "myhome.dangdang.com",
    "Referer": "http://book.dangdang.com/?_utm_brand_id=11106&_ddclickunion=460-5-biaoti|ad_type=0|sys_id=1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Upgrade-Insecure-Requests": "1",
    # 操作cookie
    "Cookie": '__permanent_id=20180401194257529455615680812733633; ddscreen=2; __ddc_15d_f=1522583046%7C!%7C_utm_brand_id%3D11106; __visit_id=20180401194405703384969867965543673; __out_refer=1522583046%7C!%7Cwww.baidu.com; permanent_key=201804011944042530227214362e7297; login_dang_code=20180401194436455509547177c0e385; USERNUM=2XtyLdy0HlE0rThuWF70qw==; login.dangdang.com=.AYH=&.ASPXAUTH=ec2QipHzLmutsuG7vQAwYEM1M7OMT7if; dangdang.com=email=MTAyNTcxMTk5NUBxcS5jb20=&nickname=x+C0uti80sC+ybbpwuQ=&display_id=7275288508254&customerid=a40RoSMU/jAag674CAAzfw==&viptype=58OG3nW+5no=&show_name=186%2A%2A%2A%2A4857; ddoy=email=1025711995%40qq.com&nickname=%C7%E0%B4%BA%D8%BC%D2%C0%BE%C9%B6%E9%C2%E4&agree_date=1&validatedflag=0&uname=18606994857&utype=1&.ALFG=on&.ALTM=1522583086; sessionID=pc_466c2da86eb2b470b36a560753d0ff58a82eac8f27009054f2949ed029f4fdbd; __dd_token_id=20180401194446469713101869786264; LOGIN_TIME=1522583091553; __ddc_1d=1522583092%7C!%7C_utm_brand_id%3D11106; __ddc_24h=1522583092%7C!%7C_utm_brand_id%3D11106; __ddc_15d=1522583092%7C!%7C_utm_brand_id%3D11106; UM_distinctid=16281067b9410cb-05b48e974659e5-33627805-13c680-16281067b95749; from=488-164325581-0; order_follow_source=P-488-1643%7C%231%7C%23222.186.160.115%252Fdangdang.html%7C%230%7C%23vLV4z340mtyd-%7C-; pos_9_end=1522583116899; pos_0_end=1522583117088; ad_ids=2592278%2C2592277%7C%231%2C1; cart_id=4000000001213959275; pos_0_start=1522583137531; cart_items_count=3; deal_token=1075252e12695e48f13b81aa4e2d354c07a6c43721bb55a9728e2d6aad71497c8e06ff0e5acecb5fd4; NTKF_T2D_CLIENTID=guest51ECC8EE-0A24-23BD-D1BD-81071C79A9E5; nTalk_CACHE_DATA={uid:dd_1000_ISME9754_121395927,tid:1522583149688133}; dest_area=country_id%3D9000%26province_id%3D135%26city_id%3D2101%26district_id%3D1350103%26town_id%3D135010308; __rpm=...1522583147022%7C...1522583258544; __trace_id=20180401194748148118777570693619382; _jzqco=%7C%7C%7C%7C%7C1.586552655.1522583045972.1522583261193.1522583268202.1522583261193.1522583268202.0.0.0.6.6'}


def get_book_info(book_shop_url, product_id, category_path):
    r = requests.get(book_shop_url, headers=head)
    author = ""
    if r.status_code != 200:
        print("获取图书数据异常，跳过!code=%s,url=%s", r.status_code, book_shop_url)
    else:
        response_html = str(r.content.decode("gbk"))
        results = re.findall(r"作者.*?出版社", response_html, re.I | re.S | re.M)
        if len(results) > 0:
            author = results[0].replace("作者：", "").replace("，出版社：", "")

    introduce = ""
    introduce_url = "http://product.dangdang.com/index.php?r=callback/detail&productId=%s&templateType=publish&describeMap=&shopId=0&categoryPath=%s" % (
        product_id, category_path)
    r = requests.get(introduce_url, headers=head)
    if r.status_code != 200:
        print("获取图书简介异常，跳过!code=%s,url=%s", r.status_code, introduce_url)
    else:
        response_json = r.json()
        html = response_json["data"]["html"]
        results = re.findall(r"content-show.*?content-show-all", html, re.I | re.S | re.M)
        if len(results) > 0:
            introduce = results[0].replace("content-show\">", "").replace("</span><span id=\"content-show-all", "")

    book_data = {}
    book_data["author"] = author
    book_data["introduce"] = introduce
    return book_data


def getOrder():
    print("正在获取订单信息")

    url = "http://myhome.dangdang.com/myOrder/list?searchType=1&statusCondition=0&timeCondition=0&page_current=1"
    r = requests.get(url, headers=head)
    if r.status_code != 200:
        print("获取列表异常，终止爬虫!code=%s", r.status_code)
        return
    response_html = str(r.content.decode("gbk"))

    order_str = ""
    results = re.findall(r"{\"orderList.*?pageinfo", response_html, re.I | re.S | re.M)
    if len(results) > 0:
        order_str = results[0].replace(",\"pageInfo", "}")

    if order_str is None or len(order_str) == 0:
        print("未获取到订单列表，终止爬虫!")
        return
    order_json = json.loads(order_str)

    order_list = order_json["orderList"]

    size = len(order_list)
    if size == 0:
        print("未找到订单信息，结束爬虫")
        return

    print("一共获取到%s条订单信息" % size)

    for i in range(size):
        order = order_list[i]
        print("正在获取第%s条订单信息" % (i + 1))

        order_id = order["order"]["orderId"]
        buy_time = order["order"]["orderCreationDate"]

        for book in order["products"]:
            book_name = book["productName"]
            book_price = book["salePrice"]
            book_url = book["productImg"]
            book_author, book_introduce = "", ""
            book_shop_url = book["productSnapshotUrl"]

            category_path = book["categoryPath"]
            product_id = book["productId"]
            book_other_data = get_book_info(book_shop_url, product_id, category_path)
            if book_other_data is not None:
                book_author = book_other_data["author"]
                book_introduce = book_other_data["introduce"]
            try:
                with connection.cursor() as cursor:
                    sql = 'INSERT INTO orders(BOOK_NAME,BOOK_AUTHOR,BOOK_PRICE,BOOK_INTRODUCE,BOOK_URL,BUY_TIME,ORDER_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)'
                    cursor.execute(sql,
                                   (book_name, book_author, book_price, book_introduce, book_url, buy_time, order_id))
                connection.commit()
            except Exception as e:
                print("数据库写入失败", e)
    print("获取订单信息完成")


if __name__ == '__main__':
    getOrder()
