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
import config

# 创建一个Chrome浏览器实例
chrome_options = Options()
chrome_options.page_load_strategy = 'eager'
chrome_options.add_argument(
    "User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 8_0 like Mac OS X) AppleWebKit/600.1.3 (KHTML, like Gecko) Version/8.0 Mobile/12A4345d Safari/600.1.4");

# chrome_options.add_argument("--incognito")  # 设置为隐私模式

chrome_options.add_extension(config.plugin_path)

# 指定ChromeDriver的路径
s = Service(executable_path=config.executable_path)

# 创建一个Chrome浏览器实例，并指定ChromeDriver的路径
driver = webdriver.Chrome(service=s, options=chrome_options)


def disconnect_wallet():
    switch_handle("leaderboard")
    driver.find_elements(By.XPATH, '//span[contains(text(),"...")]')[0].click()
    util.click(driver, By.XPATH, '//span[text()="Disconnect"]')
    time.sleep(2)


def switch_handle(keywords_str):
    keywords = keywords_str.split(",")
    window_index = 0
    loop_times = 0
    while loop_times < 10:  # 等待10s，避免窗口没来得及打开
        time.sleep(1)
        if window_index >= len(driver.window_handles):
            # 所有页面都找完后没有插件页面，打开插件页面
            window_index = 0
            if "chrome" in keywords_str:
                keyboard_c = KeyboardController()
                with keyboard_c.pressed(Key.shift, Key.alt):
                    keyboard_c.press("o")
                time.sleep(2)
                driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
                return
        driver.switch_to.window(driver.window_handles[window_index])
        for keyword in keywords:
            if keyword in driver.current_url:
                print("找到页面了，url = " + driver.current_url)
                return
        window_index = window_index + 1


class WorldStore:
    def __init__(self):
        self.account_num = 100  # 单个钱包的账户数量
        self.wallet_data_json = {}
        self.current_wallet_id = None
        self.twitter_token = None
        self.tokens = []
        self.account_index = 0

    def twitter_login(self):
        switch_handle("okx,crypto,x.com")
        driver.get("https://x.com/")
        # token 已经用完
        if len(self.tokens) == 0:
            print("没有token了")
        self.twitter_token = self.tokens[0]
        cookies = {'value': self.twitter_token, 'name': 'auth_token'}
        driver.add_cookie(cookie_dict=cookies)

        driver.get(
            "https://x.com/i/oauth2/authorize?response_type=code&client_id=aWVQSnRnalFXZHphOHo0OEVUNWc6MTpjaQ&redirect_uri=https://worldstore.mirrorworld.fun/twitter&scope=follows.read%20follows.write%20users.read%20tweet.read%20offline.access&state=BLyhYwnrDZUpXk7FVWKiuZLu3cUf5thn4mQJSS5vJ2qM&code_challenge=challenge&code_challenge_method=plain")
        time.sleep(3)

    def switch_wallet(self):
        switch_handle("chrome")
        account_element = driver.find_element(By.XPATH, '//div[contains(text(),"账户")]')
        account_index = account_element.text.replace("账户 ", "")
        account_element.click()

        next_account_index = int(account_index) + 1
        self.account_index = next_account_index
        next_account_name = str(next_account_index)
        if next_account_index < 10:
            next_account_name = "0" + next_account_name
        next_account_name = "账户 " + next_account_name
        try:
            next_account_element = driver.find_element(By.XPATH, '//div[text()="' + next_account_name + '"]')
            next_account_element.click()
        except Exception as e:
            print(e)
            if account_index == self.account_num:
                return
            target = driver.find_element(By.XPATH, '//div[text()="添加账户"]')
            driver.execute_script("arguments[0].scrollIntoView();", target)
            time.sleep(1)
            util.click(driver, By.XPATH, '//div[text()="添加账户"]')
            util.click(driver, By.XPATH, '//div[text()="' + next_account_name + '"]')

    def wallet_login(self):
        # 打开一个网址
        driver.get("https://worldstore.mirrorworld.fun/leaderboard")

        time.sleep(1)
        switch_handle("chrome")

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
            self.switch_wallet()
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
                "account_index": 1,
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

    def connect_wallet(self, account_index):
        print("正在连接第" + str(account_index) + "个钱包账号")
        switch_handle("leaderboard")

        # 通过按钮名称找到按钮元素
        util.click(driver, By.XPATH, '//button[text()="Connect Wallet"]')

        util.click(driver, By.XPATH, '//div[text()="Phantom"]')

        time.sleep(3)
        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        util.click(driver, By.XPATH, '//div[text()="连接"]')

        time.sleep(2)
        switch_handle("leaderboard")
        util.click(driver, By.XPATH, '//div[text()="Phantom"]')

        time.sleep(5)

        driver.switch_to.window(driver.window_handles[len(driver.window_handles) - 1])
        util.click(driver, By.XPATH, '//div[text()="确认"]')

        time.sleep(1)

        switch_handle("leaderboard")
        try:
            driver.find_element(By.XPATH, '//span[text()="Follow on X"]')
        except Exception as e:
            print(e)
            print("该钱包账号已被关注，跳过")
            disconnect_wallet()
            return
        ws.twitter_login()

        util.click(driver, By.XPATH, '//span[text()="Authorize app"]')

        for _ in range(5):
            if "worldstore" in driver.current_url:
                time.sleep(4)
                break
            time.sleep(2)

        wallet_data = self.wallet_data_json.get(self.current_wallet_id)
        wallet_data["account_index"] = self.account_index
        twitter_follow = wallet_data["twitter_follow"]
        twitter_follow.append(self.twitter_token)
        wallet_data["twitter_follow"] = twitter_follow
        self.wallet_data_json[self.current_wallet_id] = wallet_data
        self.write_json()

        self.tokens.remove(self.twitter_token)
        self.write_tokens()

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
    with open(config.tokens_path, 'r') as token_f:
        for token in token_f.readlines():
            ws.tokens.append(token.strip().replace('\n', ''))
    used_tokens = []
    with open(config.wallet_path, "r") as wallet_f:
        wallet_json = json.loads(wallet_f.read())
        ws.wallet_data_json = wallet_json
        for k, v in wallet_json.items():
            if len(v["twitter_follow"]) < 100:
                ws.current_wallet_id = k
            used_tokens.append(v["twitter_follow"])

    ws.tokens = [item for item in ws.tokens if item not in used_tokens]

    try:
        while True:
            if ws.current_wallet_id is not None:
                wd = wallet_json[ws.current_wallet_id]
                if "account_index" in wd:
                    ws.account_index = wd["account_index"]
                else:
                    ws.account_index = 1
            ws.wallet_login()
            for i in range(ws.account_index, ws.account_num):
                ws.connect_wallet(i + 1)
                if i == ws.account_num - 1:
                    break
                ws.switch_wallet()
            # 清空当前钱包，重新创建新的钱包
            ws.current_wallet_id = None
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        driver.close()
