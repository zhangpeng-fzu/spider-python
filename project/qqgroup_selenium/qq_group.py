import time
import requests
import re
from tkinter import *
import tkinter.messagebox
from hyper.contrib import HTTP20Adapter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from os.path import *


class SessionDriver:

    def __init__(self):
        self.browser = None

    def get_html(self, group_code):
        # cookies = {}
        try:
            self.__init_browser(group_code)
            time.sleep(10)
            # 鼠标下拉十次
            for i in range(10):
                source = self.browser.find_element_by_class_name('header')
                target = self.browser.find_element_by_class_name('footer')
                actions = ActionChains(self.browser)
                actions.drag_and_drop(source, target)
                actions.perform()
            time.sleep(5)
            return self.browser.page_source
        finally:
            self.__destroy_browser()

    def __init_browser(self, group_code):
        """
        初始化selenium浏览器
        :return:
        """
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.maximize_window()
        self.browser.get("https://qun.qq.com/member.html#gid=%s" % group_code)

    def __destroy_browser(self):
        """
        销毁selenium浏览器
        :return:
        """
        if self.browser is not None:
            pass
            self.browser.quit()


def download():
    print(qq_str)
    if qq_str is None or len(qq_str) == 0:
        tkinter.messagebox.showerror('错误', "请先提取qq号码")
        return
    filename = "qq_" + entry.get() + ".txt"
    with open(filename, 'w+') as f:
        f.write(qq_str)
    filepath = dirname(abspath(__file__)) + "/" + filename
    tkinter.messagebox.showinfo('提示', '下载成功，请查看' + filepath)


def show(response_content):
    global qq_str
    results = re.findall(r"useIcon\d+\"", response_content, re.I | re.S | re.M)
    for res in results:
        number = res.replace("useIcon", "").replace("\"", "")
        qq_str = qq_str + number + "\n"
        text.insert(END, '%s' % number)
        # 文本框向下滚动
        text.see(END)
        # 更新(不更新就一直卡在那，显示同样的内容)
        text.update()


def fetch():
    if entry.get() is None or len(entry.get()) == 0:
        tkinter.messagebox.showerror('错误', "请先输入qq群号码")
        return
    show(SessionDriver().get_html(entry.get()))


if __name__ == '__main__':
    qq_str = ""
    # 1.创建窗口
    root = Tk()

    # 2.窗口标题
    root.title('网易云音乐')

    # 3.窗口大小以及显示位置,中间是小写的x
    root.geometry('550x400+550+230')
    # 窗口显示位置
    # root.geometry('+573+286')

    # 4.标签控件
    lable = Label(root, text='请输入要QQ群号:', font=('微软雅黑', 10))
    lable.grid(row=0, column=0)

    # 5.输入控件
    entry = Entry(root, font=('微软雅黑', 20))
    entry.grid(row=0, column=1)
    button = Button(root, text='提取', width=10, font=('微软雅黑', 10), command=fetch)
    button.grid(row=0, column=3, sticky=W)

    # 6.列表框控件
    text = Listbox(root, font=('微软雅黑', 16), width=45, height=10)

    # columnspan组件所跨越的列数
    text.grid(row=1, columnspan=2)
    # 7.按钮控件
    button = Button(root, text='下载', width=10, font=('微软雅黑', 10), command=download)
    button.grid(row=2, column=0, sticky=W)

    button1 = Button(root, text='退出', width=10, font=('微软雅黑', 10), command=root.quit)
    button1.grid(row=2, column=1, sticky=E)

    root.mainloop()
