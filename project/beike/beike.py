import json
import random
import time

import requests
from bs4 import BeautifulSoup

header = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Cookie": "lianjia_uuid=0111066e-304f-45de-8f91-4f8566fe6d13; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218fae24e042896-0737d2e0a7befc-1a525637-1892970-18fae24e04314c3%22%2C%22%24device_id%22%3A%2218fae24e042896-0737d2e0a7befc-1a525637-1892970-18fae24e04314c3%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; crosSdkDT2019DeviceId=t20vkc-qg82dj-szd7wgyzcnoaxja-acbszrsch; select_city=450100; login_ucid=2000000236672197; lianjia_token=2.001026f6717498cf58018bdf40adccbf0f; lianjia_token_secure=2.001026f6717498cf58018bdf40adccbf0f; security_ticket=Hg8TL273NhyJ6ZjBn0j0eAqNTogQmiIwGDhVymEb9Q+cg/wmkT8FuAaqqnGqG3psyENqZpkBz2OpeNauWExHMU1N0IcYFMYB5H7TsTLQCEozUbLuwLDCq+3M00GoyBdRHYbGTSOhaeNGACQ6HknLUjwM2Zu1IiU0+QodQ/fvcsU=; ftkrc_=e146fd4e-ec25-424e-aaaa-6a6a976f5159; lfrc_=bfd7a325-1972-4dac-a122-6ef0e136a282",
    "Host": "nn.ke.com",
    "Referer": "https://nn.ke.com/chengjiao/",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Google Chrome\";v=\"125\", \"Chromium\";v=\"125\", \"Not.A/Brand\";v=\"24\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\""
}


def parse_response(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    ul_element = soup.find('ul', class_='listContent')
    li_elements = ul_element.find_all('li')

    for li in li_elements:
        info = {}

        # 提取标题
        title = li.find('div', class_='title').find('a').text.strip()
        info['title'] = title

        # 提取地址
        address = li.find('div', class_='address').find('div', class_='houseInfo').text.strip()
        info['address'] = address

        # 提取成交日期
        deal_date = li.find('div', class_='dealDate').text.strip()
        info['deal_date'] = deal_date

        # 提取总价
        total_price = li.find('div', class_='totalPrice').find('span', class_='number').text.strip()
        info['total_price'] = total_price

        # 提取单价
        unit_price = li.find('div', class_='unitPrice').find('span', class_='number').text.strip()
        info['unit_price'] = unit_price

        # 提取房屋信息
        deal_house_info = li.find('div', class_='dealHouseInfo')
        if deal_house_info:
            deal_house_info = deal_house_info.find('span', class_='dealHouseTxt')
            if deal_house_info:
                deal_house_info = deal_house_info.text.strip().split('\n')
                info['deal_house_info'] = [info.strip() for info in deal_house_info]
            else:
                info['deal_house_info'] = []
        else:
            info['deal_house_info'] = []

        # 提取成交周期信息
        deal_cycle_info = li.find('div', class_='dealCycleeInfo')
        if deal_cycle_info:
            deal_cycle_info = deal_cycle_info.find('span', class_='dealCycleTxt')
            if deal_cycle_info:
                deal_cycle_info = deal_cycle_info.text.strip().split('\n')
                info['deal_cycle_info'] = [info.strip() for info in deal_cycle_info]
            else:
                info['deal_cycle_info'] = []
        else:
            info['deal_cycle_info'] = []
        return info


def spider(url, retries=3):
    result = []

    for retry_time in range(retries):
        try:
            result.append(parse_response(requests.get(url, headers=header)))
        except requests.exceptions.RequestException as e:
            print(f"请求失败，正在重试第{retry_time + 1}次")
            time.sleep(1)

    return result


if __name__ == '__main__':
    total_res = []
    for i in range(25):
        page_num = str(i + 1)
        print("正在访问第" + page_num + "页")
        try:
            time.sleep(random.randint(2, 5))
            page_res = spider("https://nn.ke.com/chengjiao/pg" + page_num + "mw1/")
            total_res.append(page_res)
            print(json.dumps(page_res, ensure_ascii=False))
        except Exception as e:
            print(e)
    print(total_res)
