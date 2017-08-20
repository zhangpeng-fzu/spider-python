# -*-coding:utf8-*-

import sys
import time
from database.mysql import MySQL
from request.request_manager import requestManager

reload(sys)
sys.setdefaultencoding('utf-8')

MySQLClient = MySQL()
ids = MySQLClient.fetchmany("select * from JUGEMENT WHERE URL = ''")
urls = []
for aid in ids:
    url = "https://www.itslaw.com/api/v1/detail?timestamp=1502224564992&judgementId=" + str(
        aid[0]).replace("\n", "") + "&area=1&sortType=1&conditions=searchWord%B"
    urls.append(url)
count = len(urls)

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


def spider(url):
    judgement_id = url.split("judgementId=")[1][0:36]
    row = MySQLClient.fetchone("select * from JUGEMENT WHERE ID = '" + judgement_id + "' and URL !=''")
    if row is not None:
        return
    print("request start,url=" + url)
    head["Referer"] = head["Referer"].replace("judgementId=1", "judgementId=" + judgement_id)
    content = requestManager.get(url, head)
    if judgement_id not in content:
        print(content)
        sql = "UPDATE JUGEMENT SET URL='failed',CONTENT='""' WHERE ID='" + judgement_id + "'"  # 执行sql语句
        MySQLClient.execute(sql)
    else:
        # print("success")
        sql = "UPDATE JUGEMENT SET URL='" + url + "',CONTENT='" + content + "' WHERE ID='" + judgement_id + "'"  # 执行sql语句
        MySQLClient.execute(sql)


while True:
    try:
        aid = MySQLClient.fetchone("select * from JUGEMENT WHERE URL = ''")
        if aid is None:
            print("暂时没有新的ID啦，休息一会儿")
            time.sleep(3)
        url = "https://www.itslaw.com/api/v1/detail?timestamp=1502224564992&judgementId=" + str(
            aid[0]).replace("\n", "") + "&area=1"
        spider(url)
        time.sleep(0.3)
    except Exception, e:
        time.sleep(1)
        print(e)
