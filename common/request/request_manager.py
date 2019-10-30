# -*-coding:utf8-*-

import sys
import requests
from proxy import Proxy

reload(sys)

sys.setdefaultencoding('utf-8')

proxyClient = Proxy()
head = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'gr_user_id=593f4a3c-f92e-4a47-a6dc-27f45066b482; showSubSiteTip=false; sessionId=f7a980d9-cae9-4c30-b34a-bb65b0fd82aa; subSiteCode=bj; gr_session_id_8d9004219d790ea8=33aa13e9-f5d3-420f-ba17-f77f3d5bdbc0; Hm_lvt_e496ad63f9a0581b5e13ab0975484c5c=1502201855,1502222875,1502377663; Hm_lpvt_e496ad63f9a0581b5e13ab0975484c5c=1502723793',
    'Host': 'www.itslaw.com',
    'If-Modified-Since': 'Mon, 26 Jul 1997 05:00:00 GMT',
    'Pragma': 'no-cache',
    'Referer': 'https://www.itslaw.com/detail?judgementId=1&area=1&index=1&sortType=1&count=1543&conditions=region%2B1%2B1%2B%E5%8C%97%E4%BA%AC%E5%B8%82&conditions=caseType%2B2%2B10%2B%E5%88%91%E4%BA%8B&conditions=trialYear%2B2008%2B7%2B2008',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36'
}


class RequestManager(object):
    def __init__(self):
        self.url = ""

    @staticmethod
    def get(url, head):
        # print("request start,url=" + url)
        proxies = proxyClient.get_ip()
        html = requests.get(url, headers=head, proxies=proxies)
        # html = requests.get(url, headers=head, timeout=2)
        return str(html.content)


if __name__ == "__main__":
    requestManager = RequestManager()
    print(requestManager.get("http://cs.101.com", []))
