import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

TB_LOGIN_URL = 'https://qun.qq.com/member.html#gid=68476161'
CHROME_DRIVER = './browser/chromedriver.exe'


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

    def get_session(self, username, password):
        cookies = {}
        try:
            self.__init_browser()
            self.__switch_to_password_mode()
            time.sleep(0.5)
            self.__write_username(username)
            time.sleep(0.5)
            self.__write_password(password)
            time.sleep(0.5)
            if self.__lock_exist():
                self.__unlock()
            self.__submit()
            # 提取cookie
            for cookie in self.browser.get_cookies():
                cookies[cookie['name']] = cookie['value']
        finally:
            self.__destroy_browser()

        return cookies

    def __switch_to_password_mode(self):
        """
        切换到密码模式
        :return:
        """
        if self.browser.find_element_by_id('J_QRCodeLogin').is_displayed():
            self.browser.find_element_by_id('J_Quick2Static').click()

    def __write_username(self, username):
        """
        输入账号
        :param username:
        :return:
        """
        username_input_element = self.browser.find_element_by_id('TPL_username_1')
        username_input_element.clear()
        username_input_element.send_keys(username)

    def __write_password(self, password):
        """
        输入密码
        :param password:
        :return:
        """
        password_input_element = self.browser.find_element_by_id("TPL_password_1")
        password_input_element.clear()
        password_input_element.send_keys(password)

    def __lock_exist(self):
        """
        判断是否存在滑动验证
        :return:
        """
        return self.__is_element_exist('#nc_1_wrapper') and self.browser.find_element_by_id(
            'nc_1_wrapper').is_displayed()

    def __unlock(self):
        """
        执行滑动解锁
        :return:
        """
        bar_element = self.browser.find_element_by_id('nc_1_n1z')
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 350, 0).perform()
        time.sleep(0.5)
        self.browser.get_screenshot_as_file('error.png')
        if self.__is_element_exist('.errloading > span'):
            error_message_element = self.browser.find_element_by_css_selector('.errloading > span')
            error_message = error_message_element.text
            self.browser.execute_script('noCaptcha.reset(1)')
            raise SessionException('滑动验证失败, message = ' + error_message)

    def __submit(self):
        """
        提交登录
        :return:
        """
        self.browser.find_element_by_id('J_SubmitStatic').click()
        time.sleep(0.5)
        if self.__is_element_exist("#J_Message"):
            error_message_element = self.browser.find_element_by_css_selector('#J_Message > p')
            error_message = error_message_element.text
            raise SessionException('登录出错, message = ' + error_message)

    def __init_browser(self):
        """
        初始化selenium浏览器
        :return:
        """
        # options = webdriver.FirefoxOptions()
        options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # options.add_argument('--proxy-server=http://127.0.0.1:9000')
        # self.browser = webdriver.Firefox()
        self.browser = webdriver.Chrome(chrome_options=options)
        # self.browser.implicitly_wait(3)
        # self.browser.maximize_window()
        self.browser.get(TB_LOGIN_URL)

    def __destroy_browser(self):
        """
        销毁selenium浏览器
        :return:
        """
        if self.browser is not None:
            pass
            # self.browser.quit()

    def __is_element_exist(self, selector):
        """
        检查是否存在指定元素
        :param selector:
        :return:
        """
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False


def get_session(username, password):
    return SessionDriver().get_session(username, password)


if __name__ == '__main__':
    get_session("合美富兴数码专营店:星海", "qaz123456")
