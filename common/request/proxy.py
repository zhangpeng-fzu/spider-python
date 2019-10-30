# -*-coding:utf8-*-

import sys
import requests
import bs4
import re
from random import choice

reload(sys)

sys.setdefaultencoding('utf-8')


class Proxy(object):
    def __init__(self):
        self.ip = ''
        self.ips = []
        # 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet
        self.uas = [
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
            "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
            "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
        ]

    def get_ip(self):
        url = "http://www.xicidaili.com/nn"
        headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                   "Accept-Encoding": "gzip, deflate, sdch",
                   "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                   "Referer": "http://www.xicidaili.com",
                   "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                   }
        r = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(r.text, 'html.parser')
        data = soup.table.find_all("td")
        ip_compile = re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')  # 匹配IP
        port_compile = re.compile(r'<td>(\d+)</td>')  # 匹配端口
        ip = re.findall(ip_compile, str(data))  # 获取所有IP
        port = re.findall(port_compile, str(data))  # 获取所有端口
        self.ips.extend([":".join(i) for i in zip(ip, port)])  # 组合IP+端口，如：115.112.88.23:8080
        try:
            self.ip = choice(self.ips)
            proxies = {
                "http": self.ip
            }
        except:
            proxies = {}
        return proxies
