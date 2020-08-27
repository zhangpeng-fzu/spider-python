# -*-coding:utf-8-*-

import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from urllib.parse import quote


class SessionDriver:

    def __init__(self):
        self.browser = None

    def get_html(self, href):
        self.__init_browser()

        self.browser.get(href)
        time.sleep(2)

        return self.browser.page_source

    def __init_browser(self):
        """
        初始化selenium浏览器
        :return:
        """
        if self.browser is None:
            options = webdriver.ChromeOptions()
            self.browser = webdriver.Chrome(options=options)
            self.browser.maximize_window()
            time.sleep(5)

    def __destroy_browser(self):
        """
        销毁selenium浏览器
        :return:
        """
        if self.browser is not None:
            pass
            self.browser.quit()


chrome_session = SessionDriver()


def download(url):
    chrome_session.get_html(url)


def get_book_name(href):
    url = "https://www.qubook.net%s" % href

    try:
        # 发起请求,得到响应结果
        r = requests.get(url)

        if r.status_code != 200:
            return
        response_text = str(r.content, "gbk")
        soup = BeautifulSoup(response_text, features='html.parser')

        download_link = soup.findAll("a", text=re.compile("下载地址"))
        book_name = soup.find("h1").text

        # for li in download_link:
        # print("正在下载%s" % book_name)
        # download("https://www.qubook.net" + download_link[2].attrs["href"])
        url = "https://down.baoshuu.com/%s.rar" % quote(book_name)
        download(url)

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
        soup = BeautifulSoup(response_text, features='html.parser')

        book_link_list = soup.findAll("div", class_="ll1")[0].contents[2].findAll("a", text="下载")

        for li in book_link_list:
            get_book_name(li.attrs["href"])

    except Exception as e:
        print(e)
    finally:
        time.sleep(1)


if __name__ == '__main__':
    get_book_list(26)
