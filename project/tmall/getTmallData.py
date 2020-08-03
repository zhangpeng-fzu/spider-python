# -*- coding: utf-8 -*-
import requests
import json
import csv
import random
import re
from datetime import datetime
import time
import MySQLdb


class TM_producs(object):
    def __init__(self, storename):
        self.storename = storename
        self.url = 'https://{}.m.tmall.com'.format(storename)
        self.headers = {
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 "
                          "(KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }
        datenum = datetime.now().strftime('%Y%m%d%H%M')
        self.filename = '{}_{}.csv'.format(self.storename, datenum)
        # self.get_file()
        conn = self.getConn()
        self.init_mysql(conn)
        self.closeConn(conn)

    def get_file(self):
        '''创建一个含有标题的表格'''
        title = ['item_id', 'price', 'quantity', 'sold', 'title', 'totalSoldQuantity', 'url', 'img',
                 'titleUnderIconList']
        with open(self.filename, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=title)
            writer.writeheader()
        return

    def init_mysql(self, conn):
        cur = conn.cursor()
        cur.execute("create table shop_info(id varchar(50) ,title varchar(100),url varchar(100))")
        cur.execute("create table rom_info(id varchar(50) ,rom varchar(100),price varchar(100))")
        cur.execute(
            "create table phone_info(id varchar(50) ,shop_id varchar(50) ,title varchar(100),url varchar(100),img varchar(100),sold varchar(100),totalSoldQuantity varchar(100),price varchar(100))")
        cur.close()
        return

    def save_common_info(self, data):
        '''保存店铺信息'''
        conn = self.getConn()
        cur = conn.cursor()
        cur.execute("select * from shop_info where id='" + data.get('shop_id') + "'")
        result = cur.fetchone();
        print(result)
        if result == None:
            cur.execute("insert into shop_info values('" + data.get('shop_id') + "','" + data.get(
                'shop_title') + "','https:" + data.get('shop_Url') + "')")

        cur.close()
        conn.commit()
        conn.close()
        return

    def save_phone_info(self, data):
        '''保存手机信息'''
        conn = self.getConn()
        cur = conn.cursor()
        products = data.get('items')
        for row in products:
            # print(row)
            cur.execute("insert into phone_info values('" + str(row.get('item_id')) + "','" + str(
                data.get('shop_id')) + "','" + row.get('title') + "','https:" + row.get('url') + "','" + row.get(
                'img') + "','" + str(row.get('sold')) + "','" + str(row.get('totalSoldQuantity')) + "','" + str(
                row.get('price')) + "')")
        cur.close()
        conn.commit()
        conn.close()
        return

    def getConn(self):
        conn = MySQLdb.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='test',
            charset='utf8'
        )
        return conn

    def closeConn(self, conn):
        conn.close()

    def get_totalpage(self, key, sid, url):
        '''提取总页码数'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&shop_cn={}&ascid={}&scid={}&p=1&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        url = url + endurl.format(key, sid, sid, num)
        html = requests.get(url, headers=self.headers).text
        infos = re.findall('\(({.*})\)', html)[0]
        infos = json.loads(infos)
        totalpage = infos.get('total_page')
        self.save_common_info(infos)
        return int(totalpage)

    def get_products(self, page, key, sid, url):
        '''提取单页商品列表'''
        num = random.randint(83739921, 87739530)
        endurl = '/shop/shop_auction_search.do?sort=s&shop_cn={}&ascid={}&scid={}&p={}&page_size=12&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
        url = url + endurl.format(key, sid, sid, page, num)
        html = requests.get(url, headers=self.headers).text
        infos = re.findall('\(({.*})\)', html)[0]
        infos = json.loads(infos)
        # print(infos)
        products = infos.get('items')
        self.save_phone_info(infos)
        for row in products:
            num = random.randint(83739921, 87739530)
            detailUrl = 'https:' + row.get('url') + '&from=h5&ajson=1&_tm_source=tmallsearch&callback=jsonp_{}'
            url2 = detailUrl.format(num)
            html2 = requests.get(url2, headers=self.headers).text
            # print(html2)
            infos2 = re.findall('\(({.*})\)', html2)[0]
            infos2 = json.loads(infos2)
            # print(self.get_type(infos2))
            self.get_rom_info(infos2)

    def get_type(self, data):
        result = ''
        pid = ''
        vid = ''
        skuBase = data.get('skuBase')
        props = skuBase.get('props')
        for rom in props:
            if '套餐类型' == rom.get('name'):
                pid = rom.get('pid')
                for row in rom.get('values'):
                    if '官方标配' == row.get('name'):
                        vid = row.get('vid')
        return str(pid) + ':' + str(vid)

    def get_rom_info(self, data):
        result = ''
        pid = ''
        vid = ''
        skuBase = data.get('skuBase')
        props = skuBase.get('props')
        item = data.get('item')
        typeId = self.get_type(data)
        # if str(item.get('itemId')) == '543285442762':
        # print(props)
        for rom in props:
            if '存储容量' == rom.get('name'):
                pid = rom.get('pid')
                self.save_rom_info(data, rom, pid, item, typeId)

        return

    def save_rom_info(self, data, rom, pid, item, typeId):
        conn = self.getConn()
        cur = conn.cursor()
        for row in rom.get('values'):
            romId = str(pid) + ':' + str(row.get('vid'))
            priceId = self.get_price_id_by_rom(data, typeId, romId)
            price = self.get_price_by_price_id(data, priceId)
            rom = row.get('name')
            cur.execute("insert into rom_info values('" + str(item.get('itemId')) + "','" + str(rom) + "','" + str(
                price) + "')")
        cur.close()
        conn.commit()
        conn.close()

        return

    def get_price_id_by_rom(self, data, typeId, romId):
        result = ''
        skuBase = data.get('skuBase')
        skus = skuBase.get('skus')
        item = data.get('item')
        # if str(item.get('itemId')) == '543285442762':
        # print(skus)
        for row in skus:
            if (typeId in row.get('propPath')) and (romId in row.get('propPath')):
                result = row.get('skuId')
        return result

    def get_price_by_price_id(self, data, priceId):
        result = ''
        skuCore = data.get('skuCore')
        sku2info = skuCore.get('sku2info')
        if str(priceId) != '':
            result = sku2info.get('' + str(priceId)).get('price').get('priceText');

        return result

    def main(self):
        '''循环爬取所有页面宝贝'''
        temp = [
            {'shop_name': 'nubia', 'key': 'nubia%20%E6%89%8B%E6%9C%BA', 'sid': 758023596},
            {'shop_name': 'coolpad', 'key': 'cool%E6%89%8B%E6%9C%BA', 'sid': 1276259517},
            {'shop_name': 'zte', 'key': 'AXON%E5%A4%A9%E6%9C%BA%E7%B3%BB%E5%88%97', 'sid': 1283994122},
            {'shop_name': 'zte', 'key': 'Blade%20%E7%B3%BB%E5%88%97', 'sid': 1283994206},
            {'shop_name': 'zte', 'key': '%E8%BF%9C%E8%88%AA%E7%B3%BB%E5%88%97', 'sid': 1283994208},
            {'shop_name': 'meizu', 'key': '%E6%89%8B%E6%9C%BA%E4%B8%93%E5%8C%BA', 'sid': 747497802},
            {'shop_name': 'vivo', 'key': '%E6%89%8B%E6%9C%BA%E5%88%86%E7%B1%BB', 'sid': 1193147001},
            {'shop_name': 'oppo', 'key': '%E6%89%8B%E6%9C%BA', 'sid': 858030528},
            {'shop_name': 'xiaomi', 'key': '%E5%B0%8F%E7%B1%B3%20%E7%BA%A2%E7%B1%B3%E6%89%8B%E6%9C%BA',
             'sid': 758144452},
            {'shop_name': 'huawei', 'key': '%E6%89%8B%E6%9C%BA%E4%B8%93%E5%8C%BA', 'sid': 1022967649},
            {'shop_name': 'huaweistore', 'key': '%E6%89%8B%E6%9C%BA%E4%B8%93%E5%8C%BA', 'sid': 1201482770}
        ]
        for row in temp:
            key = row.get('key')
            sid = row.get('sid')
            url = 'https://{}.m.tmall.com'.format(row.get('shop_name'))
            total_page = self.get_totalpage(key, sid, url)
            # self.get_products(1,key,sid,url)
            for i in range(1, total_page + 1):
                self.get_products(i, key, sid, url)
                print('总计{}页商品，已经提取第{}页'.format(total_page, i))
                time.sleep(1 + random.random())


if __name__ == '__main__':
    storename = 'huaweistore'

    # storename = 'huawei'
    tm = TM_producs(storename)
    tm.main()
