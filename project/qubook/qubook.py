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
            prefs = {"download.default_directory": download_dir,
                     "profile.managed_default_content_settings.images": 2}
            options.add_experimental_option("prefs", prefs)
            options.add_argument("disable-infobars")
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

        for name in download_book_list:
            if book_name in name:
                print("【%s】已下载，跳过" % book_name)
                return

        elements = browser.find_elements_by_tag_name("a")

        status = "失败"
        files_num = len(os.listdir(download_dir))
        handle = browser.current_window_handle
        i = 0
        for element in reversed(elements):
            if "下载地址" not in element.text:
                continue
            i = i + 1
            element.click()
            time.sleep(3 * i)
            handles = browser.window_handles
            for newhandle in handles:
                # 筛选新打开的窗口B
                if newhandle != handle:
                    # 切换到新打开的窗口B
                    browser.switch_to.window(newhandle)
                    # 关闭当前窗口B
                    try:
                        browser.close()
                    except Exception as ex:
                        print(ex)
                    finally:
                        # 切换回窗口A
                        browser.switch_to_window(handles[0])
            if len(os.listdir(download_dir)) > files_num:
                time.sleep(sleep_time)
                status = "成功"
                break
        print("【%s】下载%s" % (book_name, status))

    except Exception as e:
        print(e)


# 获取小说列表
def get_book_list(category, page, end_page, retry_times):
    if page is None:
        page = 0
    while page <= end_page:
        page = page + 1
        print("正在获取第%s页数据" % page)
        url = "https://www.qubook.net/TXT/list%s_%s.html" % (category, page)

        try:
            # 发起请求,得到响应结果
            r = requests.get(url, timeout=10)

            if r.status_code != 200:
                break
            response_text = str(r.content, "gbk")
            soup = BeautifulSoup(response_text, features='html.parser')

            book_link_list = soup.findAll("div", class_="ll1")[0].contents[2].findAll("a", text="下载")

            for li in book_link_list:
                get_book_download_link(li.attrs["href"])
            retry_times = 0

        except Exception as e:
            print(e)
            retry_times = retry_times + 1
            if retry_times >= 3:
                continue
            page = page - 1
    chrome_session.destroy_browser()


def spider(download_directory, sleep, list_type, start_page, end_page):
    global download_dir
    global sleep_time

    download_dir = os.path.join(download_directory, str(list_type))
    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    sleep_time = sleep

    if not os.path.exists(download_dir):
        os.mkdir(download_dir)

    load_dowload_book_list()
    get_book_list(list_type, start_page, end_page, 0)
