# -*-coding:utf-8-*-

import time

import requests
import xlwt


class Hotel(object):
    def __init__(self, hotel_id, city, name, shop, address, gift, price, open_time, park_info, child_policy, notify,
                 detail):
        self.hotelId = hotel_id
        self.city = city
        self.name = name
        self.shop = shop
        self.gift = gift
        self.address = address
        self.price = price
        self.openTime = open_time
        self.parkInfo = park_info
        self.childPolicy = child_policy
        self.notify = notify
        self.detail = detail


city_map = {}

# 获取公司请求的http头部数据
head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    # "Content-Length": "499",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "Hm_lvt_c30cfe64c111172dcd13abe3d7532080=1519997376; SSOTOKEN=beacon!2395747A0E6290A7C016D16F63FDA1717FD64F7A7BFDD387D0C63EC8B997E0D07E069C0F275A4283C5A644447617E9B36C95450E6212CFEA437974484BB365A6; Hm_lpvt_c30cfe64c111172dcd13abe3d7532080=1519997537; JSESSIONID=3DED0C4CC0CAA1D4125D54C5B7143F61",
    "Host": "so.iptrm.com",
    "Origin": "http://so.iptrm.com",
    "Referer": "http://so.iptrm.com/app/patentlist",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


def reload_city_map(cities):
    for city in cities:
        city_map[city["id"]] = city["name"]


# 获取酒店详细信息
def get_hotel_info(code, hotel_id):
    try:
        url = "https://gift.colourfulchina.com/entry/%s/api/goods?version=2&id=%s" % (code, hotel_id)
        response = requests.get(url, head)
        if response.status_code != 200:
            print("获取酒店详细信息失败！satus_code = %s, hotel_id", response.status_code, hotel_id)
            return None
        hotel_data = response.json()
        hotel_info = hotel_data["shop"]
        detail = ""
        if "clause_text" in hotel_data:
            detail = detail + str(hotel_data["clause_text"]).split("。")[0]
            if detail is not None:
                detail = detail.split("\n")[0]
        price = ""
        open_time = ""
        for item in hotel_data["items"]:
            if "price" in item:
                price = price + item["name"] + " " + item["price"]["net"]
                if "fee" in item["price"]:
                    price = price + "+" + item["price"]["fee"]
                if "free" in item["price"]:
                    price = price + "+" + item["price"]["free"]
            price = price + "  "
            open_time = open_time + item["name"] + " " + item["opentime"] + "  "
        notify = ""
        if "tip" in hotel_info:
            notify = hotel_info["tip"]

        child_policy = ""
        if "kid" in hotel_info:
            child_policy = hotel_info["kid"]

        park_info = ""
        if "parking" in hotel_info:
            park_info = hotel_info["parking"]

        hotel = Hotel(hotel_id, "", str(hotel_info["title"]).split("|")[0], str(hotel_info["title"]).split("|")[1],
                      hotel_info["address"], "",
                      price.strip(), open_time.strip(), park_info, child_policy, notify,
                      detail)
        return hotel
    except Exception as e:
        print("获取酒店[%s]详细数据异常,message = %s" % (hotel_id, e))
        return None


def get_hotel_list(code):
    print("开始获取酒店列表")
    url = "https://gift.colourfulchina.com/entry/%s/api/summary?version=2" % code
    response = requests.get(url, head)
    if response.status_code != 200:
        print("获取酒店列表失败！satus_code = %s", response.status_code)
        return None
    json_data = response.json()
    cities = json_data["services"][0]["cities"]
    reload_city_map(cities)
    goods = json_data["goods"]
    hotel_list = []

    for good in goods:
        city = city_map[good["city_id"]]
        gift_code = good["gift_code"]
        if gift_code == "2F1":
            gift = "同行优惠"
        else:
            gift = "双人优惠"
        good_id = good["id"]
        print("正在获取酒店[%s]的详细数据" % good_id)
        hotel = get_hotel_info(code, good_id)
        if hotel is None:
            continue
        hotel.city = city
        hotel.gift = gift
        hotel_list.append(hotel)
    print("获取酒店列表完成，一共%s条酒店数据" % len(hotel_list))
    return hotel_list


def write_to_excel(hotel_list, code):
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("sheet1", cell_overwrite_ok=True)

    sheet_header = ["酒店名称", "商户", "地址", "优惠分类", "价格信息", "开餐时间", "停车信息", "儿童政策", "重要通知", "使用细则"]
    for i in range(len(sheet_header)):
        sheet.write(0, i, sheet_header[i])

    print("开始写入表格")
    row = 1
    for hotel in hotel_list:
        sheet.write(row, 0, hotel.name)
        sheet.write(row, 1, hotel.shop)
        sheet.write(row, 2, hotel.address)
        sheet.write(row, 3, hotel.gift)
        sheet.write(row, 4, hotel.price)
        sheet.write(row, 5, hotel.openTime)
        sheet.write(row, 6, hotel.parkInfo)
        sheet.write(row, 7, hotel.childPolicy)
        sheet.write(row, 8, hotel.notify)
        sheet.write(row, 9, hotel.detail)
        row = row + 1
    wb.save(code + "-" + str(int(time.time())) + ".xls")
    print("数据写入表格完成")


if __name__ == '__main__':
    code_list = ["cmb-buffet", "cmb-buffet-788"]
    for code in code_list:
        hotel_list = get_hotel_list(code)
        if hotel_list is not None:
            write_to_excel(hotel_list, code)
