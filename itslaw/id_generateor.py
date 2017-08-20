# -*-coding:utf8-*-

import requests
import sys
import time
import re
from database.mysql import MySQL

reload(sys)

sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()

urls = []
years = ["2008", "2009", "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017"]
for i in range(5, 2000)[::-1]:
    for year in years:
        startIndex = 0 + 20 * i
        url = "https://www.itslaw.com/api/v1/caseFiles?startIndex=" + str(
            startIndex) + "&countPerPage=20&sortType=1&conditions=region%2B1%2B1%2B%E5%8C%97%E4%BA%AC%E5%B8%82" \
                          "&conditions=caseType%2B2%2B10%2B%E5%88%91%E4%BA%8B" \
                          "&conditions=trialYear%2B" + year + "%2B7%2B" + year
        urls.append(url)

head = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'gr_user_id=593f4a3c-f92e-4a47-a6dc-27f45066b482; sessionId=52c47a93-1b0c-4c4f-abf3-2a7e50b1fb7b; Hm_lvt_e496ad63f9a0581b5e13ab0975484c5c=1502201855; Hm_lpvt_e496ad63f9a0581b5e13ab0975484c5c=1502202435; gr_session_id_8d9004219d790ea8=c9d63548-bf60-463f-9599-7362472a1385',
    'Host': 'www.itslaw.com',
    'If-Modified-Since': 'Mon, 26 Jul 1997 05:00:00 GMT',
    'Pragma': 'no-cache',
    'Referer': 'https://www.itslaw.com/search?searchMode=judgements&sortType=1&conditions=region%2B1%2B6%2B%E5%8C%97%E4%BA%AC%E5%B8%82&conditions=caseType%2B2%2B10%2B%E5%88%91%E4%BA%8B&searchView=text',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}


def spider(url):
    print("request start,url=" + url)
    html = requests.get(url, headers=head)
    content = str(html.content)
    if "失败" in content:
        print content
    else:
        res_tr = r'id(.*?)title'
        ids = re.findall(res_tr, content, re.S | re.M)
        for aid in ids:
            sql = "insert into JUGEMENT values('" + aid[3:39] + "','" + "" + "','" + "" + "')"  # 执行sql语句
            MySQLClient.execute(sql)


while len(urls) > 0:
    url = urls.pop()
    try:
        spider(url)
        time.sleep(2)
    except Exception, e:
        urls.append(url)
        time.sleep(1)
        print(e)
MySQLClient.close()
