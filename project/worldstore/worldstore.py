import time
import uuid

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import universal_character_recognition as AICloud
from pynput.keyboard import Key, Controller as KeyboardController
import json
import util

# 创建一个Chrome浏览器实例
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
# chrome_options.add_argument("--incognito")  # 设置为隐私模式

plugin_path = "/usr/local/bin/mcohilncbfahbmgdjkbpemcciiolgcge_2.93.0.crx"
chrome_options.add_extension(plugin_path)

# 指定ChromeDriver的路径
s = Service(executable_path="/usr/local/bin/chromedriver")

# 创建一个Chrome浏览器实例，并指定ChromeDriver的路径
driver = webdriver.Chrome(service=s, options=chrome_options)


def switch_wallet():
    keyboard_c = KeyboardController()
    with keyboard_c.pressed(Key.shift, Key.alt):
        keyboard_c.press("o")

    time.sleep(2)
    driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
    account_element = driver.find_element(By.XPATH, '//div[contains(text(),"账户")]')
    account_index = account_element.text.replace("账户 ", "")
    account_element.click()

    next_account_index = int(account_index) + 1
    next_account_name = str(next_account_index)
    if next_account_index < 10:
        next_account_name = "0" + next_account_name
    next_account_name = "账户 " + next_account_name
    util.click(driver, By.XPATH, '//div[text()="' + next_account_name + '"]')


def disconnect_wallet():
    driver.switch_to.window(driver.window_handles[0])
    driver.find_elements(By.XPATH, '//span[contains(text(),"...")]')[0].click()
    util.click(driver, By.XPATH, '//span[text()="Disconnect"]')
    time.sleep(2)


class WorldStore:
    def __init__(self):
        self.account_num = 100  # 单个钱包的账户数量
        self.wallet_data_json = {}
        self.current_wallet_id = None
        self.twitter_token = None
        self.tokens = []

    def twitter_login(self):
        driver.switch_to.window(driver.window_handles[1])
        driver.get("https://twitter.com/i/flow/login?redirect_after_login=%2Fhome")
        # token 已经用完
        if len(self.tokens) == 0:
            print("没有token了")
            driver.quit()
        self.twitter_token = self.tokens[0]
        cookies = {'value': self.twitter_token, 'name': 'auth_token'}
        driver.add_cookie(cookie_dict=cookies)
        driver.get("https://twitter.com")

        time.sleep(2)

    def wallet_login(self):
        # 打开一个网址
        driver.get("https://worldstore.mirrorworld.fun/leaderboard")

        time.sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        if self.current_wallet_id is not None:
            util.click(driver, By.XPATH, '//span[text()="导入已有钱包"]')
            util.click(driver, By.XPATH, '//div[text()="助记词或私钥"]')
            time.sleep(2)
            current_wallet_data = self.wallet_data_json[self.current_wallet_id]
            word_list = current_wallet_data["word_list"]
            for i, password_input in enumerate(driver.find_elements(By.TAG_NAME, "input")):
                password_input.send_keys(word_list[i])
            time.sleep(3)
            util.click(driver, By.XPATH, '//span[text()="确认"]')
            time.sleep(3)
            for password_input in driver.find_elements(By.TAG_NAME, "input"):
                password_input.send_keys("12345678")
            util.click(driver, By.XPATH, '//span[text()="确认"]')
            util.click(driver, By.XPATH, '//span[text()="设为默认钱包"]')
            util.click(driver, By.XPATH, '//span[text()="开启你的 Web3 之旅"]')
            driver.close()
        else:
            util.click(driver, By.XPATH, '//span[text()="创建新钱包"]')
            util.click(driver, By.XPATH, '//div[text()="助记词"]')
            for password_input in driver.find_elements(By.TAG_NAME, "input"):
                password_input.send_keys("12345678")

            util.click(driver, By.XPATH, '//span[text()="确认"]')
            util.click(driver, By.XPATH, '//span[text()="设为默认钱包"]')
            util.click(driver, By.XPATH, '//span[text()="开启你的 Web3 之旅"]')
            util.click(driver, By.XPATH, '//span[text()="立即备份"]')

            driver.find_element(By.TAG_NAME, "input").send_keys("12345678")
            util.click(driver, By.XPATH, '//span[text()="确认"]')

            util.click(driver, By.CLASS_NAME, "okx-wallet-plugin-eye")
            time.sleep(1)
            word_dict = {}
            wallet_data = {
                "word_list": [],
                "word_index": [],
                "twitter_follow": [],
                "id": str(uuid.uuid4())

            }
            for i in range(12):
                canvas_js = 'return document.getElementsByTagName("canvas")[' + str(i) + '].toDataURL("image/png");'
                # 执行 JS 代码并拿到图片 base64 数据
                im_info = driver.execute_script(canvas_js)  # 执行js文件得到带图片信息的图片数据
                im_base64 = im_info.split(',')[1]
                word = AICloud.request(str(i), im_base64)
                word_dict[str(i + 1)] = word
                wallet_data["word_list"].append(word)
            util.click(driver, By.XPATH, '//span[text()="我已记录完毕"]')
            time.sleep(1)
            for word_element in driver.find_elements(By.XPATH, '//div[contains(text(),"#")]'):
                index = word_element.text.replace("#", "")
                wallet_data["word_index"].append(index)
                util.click(driver, By.XPATH, '//div[text()="' + word_dict[index] + '"]')
            self.wallet_data_json[wallet_data["id"]] = wallet_data
            self.current_wallet_id = wallet_data["id"]
            self.write_json()
            util.click(driver, By.XPATH, '//div[text()="工具集"]')
            util.click(driver, By.XPATH, '//div[text()="批量添加账户"]')

            time.sleep(3)
            driver.switch_to.window(driver.window_handles[2])
            driver.find_elements(By.TAG_NAME, "input")[3].send_keys(str(self.account_num - 1))
            util.click(driver, By.XPATH, '//span[text()="确定"]')
            time.sleep(self.account_num)
            driver.close()

    def connect_wallet(self, account_index):
        print("正在连接第" + str(account_index) + "个钱包账号")
        driver.switch_to.window(driver.window_handles[0])

        # 通过按钮名称找到按钮元素
        util.click(driver, By.XPATH, '//button[text()="Connect Wallet"]')

        util.click(driver, By.XPATH, '//div[text()="Phantom"]')

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        util.click(driver, By.XPATH, '//div[text()="连接"]')

        time.sleep(2)
        driver.switch_to.window(driver.window_handles[0])
        util.click(driver, By.XPATH, '//div[text()="Phantom"]')

        time.sleep(3)

        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        util.click(driver, By.XPATH, '//div[text()="确认"]')

        driver.switch_to.window(driver.window_handles[0])
        util.click(driver, By.XPATH, '//span[text()="Follow on X"]')

        driver.switch_to.window(driver.window_handles[2])
        util.click(driver, By.XPATH, '//span[text()="Authorize app"]')
        time.sleep(10)

        wallet_data = self.wallet_data_json.get(self.current_wallet_id)
        twitter_follow = wallet_data["twitter_follow"]
        twitter_follow.append(self.twitter_token)
        wallet_data["twitter_follow"] = twitter_follow
        self.wallet_data_json[self.current_wallet_id] = wallet_data
        self.write_json()

        self.tokens.remove(self.twitter_token)
        self.write_tokens()

        driver.close()
        disconnect_wallet()

    def write_json(self):
        with open("wallet.json", "w") as f:
            print(self.wallet_data_json)
            json.dump(self.wallet_data_json, f)

    def write_tokens(self):
        with open("tokens.txt", "w") as f:
            for t in self.tokens:
                f.write(t + "\n")


if __name__ == '__main__':
    ws = WorldStore()

    with open('tokens.txt', 'r') as token_f:
        for token in token_f.readlines():
            ws.tokens.append(token.strip().replace('\n', ''))
    used_tokens = []
    with open("wallet.json", "r") as wallet_f:
        wallet_json = json.loads(wallet_f.read())
        ws.wallet_data_json = wallet_json
        for k, v in wallet_json.items():
            if len(v["twitter_follow"]) < 100:
                ws.current_wallet_id = k
            used_tokens.append(v["twitter_follow"])

    ws.tokens = [item for item in ws.tokens if item not in used_tokens]

    try:
        ws.wallet_login()
        for i in range(ws.account_num):
            ws.twitter_login()
            ws.connect_wallet(i + 1)
            if i == ws.account_num - 1:
                break
            switch_wallet()
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        driver.close()
