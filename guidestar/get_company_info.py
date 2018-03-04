# -*-coding:utf8-*-

import sys
import requests
import threadpool
import time
import re
from bs4 import BeautifulSoup
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
MySQLClient.set_table("guidestar")

head = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'ki_r=; D_IID=94834CDF-C931-3064-B649-41961E3BA689; D_UID=23AF5DAB-95A9-3D5C-8EA2-51C863072D66; D_SID=218.106.154.158:NrtZxzJf/+Hp+nLBPX4cr5f/6dyOSWUhBj7c1p1nr0Q; ASP.NET_SessionId=wx2vrqcyqdzel2fr1fnpm3pl; _vwo_uuid_v2=EDB84B3ABEE1E9EB8649F902C6B241B6|27d9b667d38e51358f44f987a7753e91; __hstc=126119634.a20327142f01f4d6c3b16ded8852eb24.1515560134534.1515560134534.1515560134534.1; __hssrc=1; hubspotutk=a20327142f01f4d6c3b16ded8852eb24; D_ZID=97A1EF18-AB6A-37DA-9565-8A7EE917CE19; D_ZUID=DA852CA1-6D8F-30F7-82BD-00D31C90B04F; D_HID=A4B35261-78D7-30A5-B57D-39044DA0BB43; messagesUtk=a20327142f01f4d6c3b16ded8852eb24; ki_t=1515560105905%3B1515560105905%3B1515562401580%3B1%3B10; __atuvc=6%7C2; __atuvs=5a559ca907464277005; mp_5d9e4f46acaba87f5966b8c0d2e47e6e_mixpanel=%7B%22distinct_id%22%3A%20%22160de6c64b21e0-0cec72cb684712-5a442916-15f900-160de6c64b47e%22%2C%22%24initial_referrer%22%3A%20%22https%3A%2F%2Fwww.guidestar.org%2Fprofile%2F45-2308357%22%2C%22%24initial_referring_domain%22%3A%20%22www.guidestar.org%22%7D; __hssc=126119634.4.1515560134535; mp_mixpanel__c=6',
    'Host': 'www.guidestar.org',
    'Pragma': 'no-cache',
    'Referer': 'https://www.guidestar.org/profile/45-2308357',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def get_company_info(ein):
    print "正在获取EIN:%s的公司信息" % ein
    r = None
    url = "https://www.guidestar.org/profile/" + ein
    try:
        r = requests.get(url, headers=head)
        print r.content
        content = str(r.content)
        results = re.findall(r"<title>.*?</title>", content, re.I | re.S | re.M)
        if len(results) != 0:
            name = results[0].replace("<title>", "").replace("</title>", "")
        else:
            name = ""
        print "获取EIN:%s的公司信息完成" % ein
        return "success"
    except Exception, e:
        print e
        print r.content
        print "=====================获取EIN:%s的公司信息完成===========================" % ein
        # return 0


get_company_info("99-0267393")
# while True:
#
#     # user_id = MySQLClient.fetchone("SELECT EIN FROM company WHERE URL is NULL ")[0]
#     if get_company_info(user_id) is None:
#         time.sleep(30)
