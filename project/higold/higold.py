# -*-coding:utf-8-*-

import requests
import json
import re
import xlwt
import time
import os
from bs4 import BeautifulSoup
from threadpool import *


class HigoldProducts(object):
    def __init__(self):
        self.category_list_url = "https://pc.higoldcloud.com/Client/category-list"
        self.good_list_url = "https://pc.higoldcloud.com/Client/Goods/goodsList?search_content=&sort=&page=%s&step=20&category_id=%s"
        self.good_detail_url = "https://www.higoldcloud.com/Client/Goods/goodsContent?goods_id=%s"
        self.headers = {
            "cookie": "client_session_id=64fd146085918d582b3209a65ede9799; session_id=599697e636095c8c12990fd7aa6454a7; _TOKEN=d792eb06e7c73ba98850b42006bc05f99f7dac22535a21a0bf66275a3878afa8%2BjivQpUbuMEQbUdSEnMcqeE50afT5i5C3NqVx46ZpR%2Fn7b96wqMyh%2B5jKEXGjp5efj59hcJMGl%2FLqVu%2Frrv2cimA90kbsBekBFOyPCTJXMvtkLvN4LCqbDzvgTeAKUPUnPPehY7GEXiaULFyRXbPexxkjwx2I4V%2FLUmKcrxMgoYo%3D; autologin=false; gr_user_id=a942b001-1bd9-45a1-a10a-95757f336d02; gr_session_id_b9c76468acc54288bfd0292976a2514d=514d22f7-b7b6-4e9b-8217-209ca0893c48; gr_cs1_514d22f7-b7b6-4e9b-8217-209ca0893c48=user_id%3Anm5580946; gr_session_id_b9c76468acc54288bfd0292976a2514d_514d22f7-b7b6-4e9b-8217-209ca0893c48=true",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36",
            "host": "pc.higoldcloud.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
        }
        self.pool = ThreadPool(5)

        write_book = xlwt.Workbook()
        data_sheet = write_book.add_sheet('sheet1')
        excel_head = ["一级分类名", "二级分类名", "商品名称", "商品地址", "组合名称", "价格", "起订量", "商品编号"]
        for i in range(len(excel_head)):
            data_sheet.write(0, i, excel_head[i])
        self.write_book = write_book
        self.data_sheet = data_sheet
        self.row = 0
        self.book_name = "商品数据-%s.csv" % str(int(time.time()))
        self.download_path = ""

    def get_categories(self):
        r = requests.get(self.category_list_url, headers=self.headers, timeout=10)
        response_text = str(r.content, "utf-8")
        soup = BeautifulSoup(response_text, features='html.parser')
        menu_level_1_data = json.loads(soup.find("div", id="menu-level-1-data").text)

        menu_level_1_map = {}
        for menu_level_1 in menu_level_1_data:
            menu_level_1_map[menu_level_1["category_id"]] = menu_level_1["category_name"]

        menu_level_2_data = json.loads(soup.find("div", id="menu-level-2-data").text)

        for menu_level_2 in menu_level_2_data:
            first_level = menu_level_1_map[menu_level_2["parent_id"]]
            second_level = menu_level_2["category_name"]

            print("正在抓取【%s/%s】" % (first_level, second_level))
            category_goods = []
            self.get_category_product(menu_level_2["category_id"], 1, category_goods)
            for category_good in category_goods:
                category_good["first_level"] = first_level
                category_good["second_level"] = second_level
            if len(category_goods) > 0:
                self.write_excel(category_goods)
                self.save_image(category_goods)

    def get_category_product(self, category_id, page, goods):
        print("正在抓取第%s页商品数据，category_id=%s" % (page, category_id))
        url = self.good_list_url % (page, category_id)
        try:
            r = requests.get(url, headers=self.headers, timeout=10)
        except Exception as e:
            print("获取分类【%s】下的第%s页产品失败,e=%s" % (category_id, page, e))
            return
        goods_data = r.json()["data"]

        for good in goods_data["list"]:
            self.get_good_detail(good["goods_id"], goods)

        total_page = int(goods_data["count"]) / 20 if int(goods_data["count"]) % 20 == 0 else int(int(
            goods_data["count"]) / 20) + 1
        if total_page <= goods_data["cpage"]:
            return
        page = page + 1
        self.get_category_product(category_id, page, goods)

    def get_good_detail(self, good_id, goods):
        try:
            r = requests.get(self.good_detail_url % good_id, headers=self.headers, timeout=10)
        except Exception as e:
            print("抓取商品【%s】失败，e=%s" % (good_id, e))
            return

        good_detail = r.json()["data"]

        options_map = {
            "0": "订货价"
        }
        # 获取option
        for multi_data in good_detail["multi_data"]:
            if not multi_data:
                continue
            for option in multi_data["options"]:
                options_map[option["options_id"]] = option["options_name"]

        for option in good_detail["options_data"]:
            option_ids = option["options_id"].split(",")

            option_name = ""
            for option_id in option_ids:
                option_name = option_name + "/" + options_map[option_id]
            if len(option_name) > 0:
                option_name = option_name[1:]

            units = good_detail[option["units"]]
            goods.append({
                "title": good_detail["goods_name"],
                "url": "https://pc.higoldcloud.com/Client/Goods/detail/%s" % good_id,
                "option_name": option_name,
                "option_price": option["whole_price"] + "/" + units,
                "min_order": good_detail["min_order"] + units,
                "id": good_id,
                "resource": good_detail["resource"],
                "content": good_detail["content"]
            })
        print("已抓取商品【%s】" % good_detail["goods_name"])

    def write_excel(self, category_goods):

        for j in range(len(category_goods)):
            category_good = category_goods[j]
            row = self.row + 1
            self.data_sheet.write(row, 0, category_good["first_level"])
            self.data_sheet.write(row, 1, category_good["second_level"])
            self.data_sheet.write(row, 2, category_good["title"])
            self.data_sheet.write(row, 3, category_good["url"])
            self.data_sheet.write(row, 4, category_good["option_name"])
            self.data_sheet.write(row, 5, category_good["option_price"])
            self.data_sheet.write(row, 6, category_good["min_order"])
            self.data_sheet.write(row, 7, category_good["id"])
            self.row = row

        self.write_book.save(self.book_name)

    @staticmethod
    def validate_title(title):
        re_str = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
        new_title = re.sub(re_str, "-", title)  # 替换为下划线
        return new_title

    def save_image(self, category_goods):
        if not os.path.exists(category_goods[0]["first_level"]):
            os.mkdir(category_goods[0]["first_level"])
        second_level_dir = os.path.join(category_goods[0]["first_level"], category_goods[0]["second_level"])
        if not os.path.exists(second_level_dir):
            os.mkdir(second_level_dir)

        for good in category_goods:
            save_path = os.path.join(second_level_dir, self.validate_title(good["title"]))
            if not os.path.exists(save_path):
                os.mkdir(save_path)

            soup = BeautifulSoup(good["content"], features='html.parser')
            content_images = soup.findAll("img")

            if len(content_images) > 0:
                detail_image_path = os.path.join(save_path, "详情图")
                if not os.path.exists(detail_image_path):
                    os.mkdir(detail_image_path)
                if len(os.listdir(detail_image_path)) < len(content_images):
                    self.download_path = detail_image_path
                    my_requests = makeRequests(self.download_image, content_images)
                    [self.pool.putRequest(req) for req in my_requests]
                    self.pool.wait()

            if len(good["resource"]) > 0:
                main_image_path = os.path.join(save_path, "主图")
                if not os.path.exists(main_image_path):
                    os.mkdir(main_image_path)
                if len(os.listdir(main_image_path)) < len(good["resource"]):
                    self.download_path = main_image_path
                    my_requests = makeRequests(self.download_image, good["resource"])
                    [self.pool.putRequest(req) for req in my_requests]
                    self.pool.wait()

            print("商品【%s】的图片已保存" % good["title"])

    def download_image(self, image):
        try:
            if isinstance(image, str):
                src = image
            else:
                src = image.attrs["src"]

            blob = requests.get(src, timeout=10)
            with open(os.path.join(self.download_path, os.path.basename(src.split("?")[0])),
                      'wb') as file:
                file.write(blob.content)

        except Exception as e:
            print(e)


if __name__ == '__main__':
    HigoldProducts().get_categories()
    # HigoldProducts().get_good_detail("8379291", [])
