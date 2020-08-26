# -*-coding:utf-8-*-

import time
import requests
from bs4 import BeautifulSoup


def download(book_name):
    url = "https://down.baoshuu.com/%s.rar" % book_name
    file_name = "book/" + book_name + ".rar"

    header = {
        "Cookie": "__cfduid=dabf8094d0c56b467385901670bab03cc1598437087",
        "Host": "down.baoshuu.com",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br"
    }
    r = requests.get(url=url, headers=header)

    if r.status_code != 200:
        return

    with open(file_name, "wb") as code:
        code.write(r.content)


def get_book_name(href):
    url = "https://www.qubook.net%s" % href

    try:
        # 发起请求,得到响应结果
        r = requests.get(url)

        if r.status_code != 200:
            return
        response_text = str(r.content, "gbk")
        soup = BeautifulSoup(response_text)

        book_name = soup.find("h1").text
        download(book_name)

    except Exception as e:
        print(e)
    finally:
        time.sleep(0.1)


# 通过获取专利授权数量
def get_book_list(category):
    page = 1
    url = "https://www.qubook.net/TXT/list%s_%s.html" % (category, page)

    try:
        # 发起请求,得到响应结果
        r = requests.get(url)

        if r.status_code != 200:
            return
        response_text = str(r.content, "gbk")
        soup = BeautifulSoup(response_text)

        book_link_list = soup.findAll("div", class_="ll1")[0].contents[2].findAll("a", text="下载")

        for li in book_link_list:
            get_book_name(li.attrs["href"])

    except Exception as e:
        print(e)
    finally:
        time.sleep(1)


if __name__ == '__main__':
    get_book_list(26)
