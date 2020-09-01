# -*-coding:utf-8-*-

import time
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from urllib.parse import quote
import os

# 下文文件目录
download_dir = ""
# 下载文件等待时间
sleep_time = 5


class SessionDriver:

    def __init__(self):
        self.browser = None

    def get_html(self, href):
        self.init_browser()

        self.browser.get(href)

        return self.browser

    def init_browser(self):
        global download_dir
        """
        初始化selenium浏览器
        :return:
        """
        if self.browser is None:
            options = webdriver.ChromeOptions()
            prefs = {"download.default_directory": download_dir}
            options.add_experimental_option("prefs", prefs)
            self.browser = webdriver.Chrome(options=options)
            self.browser.maximize_window()
            self.browser.set_page_load_timeout(30)
            time.sleep(5)

    def destroy_browser(self):
        """
        销毁selenium浏览器
        :return:
        """
        if self.browser is not None:
            pass
            self.browser.quit()


chrome_session = SessionDriver()

download_book_list = []


def load_dowload_book_list():
    files = os.listdir(download_dir)
    for file in files:
        if not os.path.isdir(file) and file.endswith(".rar"):
            download_book_list.append(file)


def get_book_download_link(href):
    url = "https://www.qubook.net%s" % href

    try:
        # 发起请求,得到响应结果
        browser = chrome_session.get_html(url)

        soup = BeautifulSoup(browser.page_source, features='html.parser')

        book_name = soup.find("h1").text.split("[")[0].strip()

        if book_name + ".rar" in download_book_list:
            return

        elements = browser.find_elements_by_tag_name("a")

        status = "失败"
        files_num = len(os.listdir(download_dir))
        for element in elements:
            if "下载地址" not in element.text:
                continue
            element.click()
            time.sleep(5)
            if len(os.listdir(download_dir)) > files_num:
                time.sleep(sleep_time)
                break
        print("【%s】下载%s" % (book_name, status))

    except Exception as e:
        print(e)
    finally:
        time.sleep(0.1)


# 获取小说列表
def get_book_list(category, page):
    if page is None:
        page = 0
    while True:
        page = page + 1
        print("正在获取第%s页数据" % page)
        url = "https://www.qubook.net/TXT/list%s_%s.html" % (category, page)

        try:
            # 发起请求,得到响应结果
            r = requests.get(url)

            if r.status_code != 200:
                break
            response_text = str(r.content, "gbk")
            soup = BeautifulSoup(response_text, features='html.parser')

            book_link_list = soup.findAll("div", class_="ll1")[0].contents[2].findAll("a", text="下载")

            for li in book_link_list:
                get_book_download_link(li.attrs["href"])

        except Exception as e:
            print(e)
            break
    chrome_session.destroy_browser()


def spider(download_directory, sleep, list_type, start_page):
    global download_dir
    global sleep_time

    download_dir = os.path.join(download_directory , str(list_type))
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    sleep_time = sleep

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    load_dowload_book_list()
    get_book_list(list_type, start_page)
