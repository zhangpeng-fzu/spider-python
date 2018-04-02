# _*_coding:utf-8_*_

import json
import re
import time

import pymysql
import requests
import xlwt

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
    "Cookie": 'deal_token=19a59f27b23e5808206e04ad6b5252495eae2bdaab03c0aea688c94ac592ad57bee738ea216b69a213; __permanent_id=20180401225745665259983480095179524; from=419-912065%7C00D060245b72bf88dc4d; order_follow_source=P-419-9120%7C%231%7C%23p.gouwubang.com%252Fl%253Fl%253Dclsnkqu%2521gz6dkz446wbqnwvyrwwopn4vntpspnm2p7ptyq4dumbqg5a%25216ybwnsubpkzsyqb5rwwoptst%7C%230%7C%23k0IYX09vqUD0-%7C-; ddscreen=2; dest_area=country_id%3D9000%26province_id%3D111%26city_id%20%3D0%26district_id%3D0%26town_id%3D0; __ddc_15d_f=1522594653%7C!%7C_ddclickunion%3D419-912065%257C00D060245b72bf88dc4d; permanent_key=20180401225754955479233526b18c6a; USERNUM=K4mtLKTcoh9ysJnelMzLRw==; login.dangdang.com=.AYH=&.ASPXAUTH=xVpdBxoFnXNnE4rXKk+TQxoY0Wu8GVDB6z/39VgixjLLH0dHKeuVxA==; dangdang.com=email=MTMxNDI3NTU4NDAxNTA5NEBkZG1vYmlscGhvbmVfX3VzZXIuY29t&nickname=&display_id=2883729859510&customerid=qGzk9XdcZ59HLDnty65wIQ==&viptype=Dpx2Hx+2cqw=&show_name=131%2A%2A%2A%2A5840; ddoy=email=1314275584015094%40ddmobilphone__user.com&nickname=&agree_date=1&validatedflag=0&uname=13142755840&utype=1&.ALFG=on&.ALTM=1522594693; sessionID=pc_cbdccdd2ba19c56446fad7b8f458823dad1c8bb60ddcc8ff092f4c8ced6a11ee; __dd_token_id=20180401225813839652240377fab5cd; __ddc_1d=1522594678%7C!%7C_ddclickunion%3D419-912065%257C00D060245b72bf88dc4d; __ddc_24h=1522594678%7C!%7C_ddclickunion%3D419-912065%257C00D060245b72bf88dc4d; __ddc_15d=1522594678%7C!%7C_ddclickunion%3D419-912065%257C00D060245b72bf88dc4d; __rpm=login_page.login_password_div..1522594670631%7Cmix_317715...1522594681023; LOGIN_TIME=1522594682423; _jzqco=%7C%7C%7C%7C%7C1.2014261426.1522594682698.1522594716825.1522594915333.1522594716825.1522594915333.0.0.0.3.3'
}


def get_book_info(book_shop_url, product_id, category_path):
    r = requests.get(book_shop_url, headers=head)
    author = ""
    if r.status_code != 200:
        print("获取图书数据异常，跳过!code=%s,url=%s", r.status_code, book_shop_url)
    else:
        try:
            response_html = str(r.content.decode("gb18030", errors='ignore'))
            results = re.findall(r"作者.*?出版社", response_html, re.I | re.S | re.M)
            if len(results) > 0:
                author = results[0].replace("作者：", "").replace("，出版社", "").replace(" 著", "")
        except Exception as e:
            print(e)
            author = ""

    introduce = ""
    introduce_url = "http://product.dangdang.com/index.php?r=callback/detail&productId=%s&templateType=publish&describeMap=&shopId=0&categoryPath=%s" % (
        product_id, category_path)
    r = requests.get(introduce_url, headers=head)
    if r.status_code != 200:
        print("获取图书简介异常，跳过!code=%s,url=%s", r.status_code, introduce_url)
    else:
        response_json = r.json()
        html = response_json["data"]["html"]
        results = re.findall(r"内容简介.*?作者简介", html, re.I | re.S | re.M)
        if len(results) > 0:
            introduce = results[0].replace("内容简介", "").replace("作者简介", "").replace(
                "</span></div><div class=\"descrip\">", "") \
                .replace("<span id=\"content-all\">", "").replace("<span id=\"content-show\">", "").replace(
                "<div id=\"authorIntroduction\" class=\"section\"><div class=\"title\"><span>", "").replace("</span>",
                                                                                                            "").replace(
                "&nbsp;", "")

    book_data = {"author": author, "introduce": introduce}
    return book_data


def get_order():
    print("正在获取订单信息")
    record_list = []
    url = "http://myhome.dangdang.com/myOrder/list?searchType=1&statusCondition=0&timeCondition=0&page_current=1"
    r = requests.get(url, headers=head)
    if r.status_code != 200:
        print("获取列表异常，终止爬虫!code=%s", r.status_code)
        return record_list

    try:
        response_html = str(r.content.decode("gbk"))
    except Exception as e:
        print("解析列表异常，终止爬虫!")
        return record_list

    order_str = ""
    results = re.findall(r"{\"orderList.*?pageinfo", response_html, re.I | re.S | re.M)
    if len(results) > 0:
        order_str = results[0].replace(",\"pageInfo", "}")

    if order_str is None or len(order_str) == 0:
        print("未获取到订单列表，终止爬虫!")
        return record_list
    order_json = json.loads(order_str)

    order_list = order_json["orderList"]

    size = len(order_list)
    if size == 0:
        print("未找到订单信息，结束爬虫")
        return record_list

    print("一共获取到%s条订单信息" % size)

    for i in range(size):
        order = order_list[i]
        print("正在获取第%s条订单信息" % (i + 1))

        order_id = order["order"]["orderId"]
        buy_time = order["order"]["orderCreationDate"]

        book_list = order["products"]
        print("===>该订单一共有%s本图书" % len(book_list))
        for k in range(len(book_list)):
            record = []
            book = book_list[k]
            print("===>正在获取第%s本图书的信息" % (k + 1))
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
            record.append(book_name)
            record.append(book_author)
            record.append(book_price)
            record.append(book_introduce)
            record.append(book_url)
            record.append(buy_time)
            record.append(order_id)

            record_list.append(record)
            # try:
            #     with connection.cursor() as cursor:
            #         sql = 'INSERT INTO orders(BOOK_NAME,BOOK_AUTHOR,BOOK_PRICE,BOOK_INTRODUCE,BOOK_URL,BUY_TIME,ORDER_ID) VALUES (%s,%s,%s,%s,%s,%s,%s)'
            #         cursor.execute(sql,
            #                        (book_name, book_author, book_price, book_introduce, book_url, buy_time, order_id))
            #     connection.commit()
            # except Exception as e:
            #     print("数据库写入失败", e)
    print("获取订单信息完成")
    return record_list


if __name__ == '__main__':
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("订单", cell_overwrite_ok=True)

    sheet_header = ["书名", "作者", "价格", "简介", "图片链接", "购买时间", "订单ID"]
    for i in range(len(sheet_header)):
        sheet.write(1, i, sheet_header[i])

    record_list = get_order()

    print("开始写入表格")
    row = 2
    for record in record_list:
        for i in range(len(sheet_header)):
            sheet.write(row, i, record[i])
        row = row + 1
    wb.save(str(int(time.time())) + ".xls")
    print("数据写入表格完成")
