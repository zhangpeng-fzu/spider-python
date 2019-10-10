import time
import requests
from hyper.contrib import HTTP20Adapter
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

TB_LOGIN_URL = 'https://qun.qq.com/member.html#gid=68476161'


class SessionException(Exception):
    """
    会话异常类
    """

    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class SessionDriver:

    def __init__(self):
        self.browser = None

    def get_session(self):
        cookies = {}
        try:
            self.__init_browser()
            time.sleep(15)
            # 提取cookie
            for cookie in self.browser.get_cookies():
                cookies[cookie['name']] = cookie['value']
        finally:
            print("登录结束")
            # self.__destroy_browser()

        return cookies

    def __init_browser(self):
        """
        初始化selenium浏览器
        :return:
        """
        options = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(chrome_options=options)
        self.browser.maximize_window()
        self.browser.get(TB_LOGIN_URL)

    def __destroy_browser(self):
        """
        销毁selenium浏览器
        :return:
        """
        if self.browser is not None:
            pass
            # self.browser.quit()


def getHeaders():
    head = {
        ":authority": "qun.qq.com",
        ":method": "POST",
        ":path": "/cgi-bin/qun_mgr/search_group_members",
        ":scheme": "https",
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://qun.qq.com",
        "pragma": "no-cache",
        "referer": "https://qun.qq.com/member.html",
        "x-requested-with": "XMLHttpRequest",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.328.186 Safari/537.36",
        "Cookie": "tvfe_boss_uuid=8ea7f36b961a77bd; pgv_pvi=5076150272; RK=dm9nENDvbE; ptcz=84d682276123b625c0396ba101442f49f8ff6ceac6a4ced492aa4e82aa2f29d9; pgv_pvid=544805496; 3g_guest_id=-8814521039636643840; o_cookie=1025711995; pac_uid=1_1025711995; h_uid=h587431518504640992; pgv_info=ssid=s8714874972; ied_qq=o1025711995; ts_last=qun.qq.com/member.html; ts_uid=7881624249; pgv_si=s2987964416; uin=o0027935615; skey=@DGzbQtnFW; p_uin=o0027935615; pt4_token=Jcb5TTmKvN0yyVoA-y2YKaropB*edFGJOO46CMsSoG0_; p_skey=mu7RupLMEcXoaFOMnjJJRGobrT2aqLz73qS3Wp-*Z0s_; ts_refer=xui.ptlogin2.qq.com/cgi-bin/xlogin; traceid=8e98e3c989"}
    return head


def get_group_data():
    form_data = {"gc": "68476161", "st": "0", "end": "20", "sort": "0", "bkn": "1232597468"}
    sessions = requests.session()
    sessions.mount('https://qun.qq.com/cgi-bin/qun_mgr/search_group_members', HTTP20Adapter())
    r = sessions.post('https://qun.qq.com/cgi-bin/qun_mgr/search_group_members', data=form_data, headers=getHeaders())
    # 发起请求,得到响应结果
    response_json = r.json()
    return response_json


if __name__ == '__main__':
    # print(SessionDriver().get_session())
    print(get_group_data())
