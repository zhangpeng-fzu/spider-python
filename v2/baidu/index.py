# -*-coding:utf8-*-

import re
import threading
import time
import urllib

import requests
from pyExcelerator import *

reload(sys)

sys.setdefaultencoding('utf-8')

head = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'BAIDUID=6A2233F5D9CFF726551537637276E53D:FG=1; BIDUPSID=6A2233F5D9CFF726551537637276E53D; PSTM=1488033252; sugstore=1; __cfduid=ddb8837e8a68e139969738c68f1afecea1497107899; MCITY=-214%3A131%3A; BDUSS=h6ZTFEcWdNN3VPYXBxMndNbGxZfmFUZ3dUZllWOU4wak44M2pPMlMyfjRDQ2hhTVFBQUFBJCQAAAAAAAAAAAEAAAC-Qrguz~50ZWFycwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAPh7AFr4ewBaTz; BD_HOME=1; BD_UPN=123253; H_PS_645EC=b5a4Y0dIF5j3f64Z665ZFrF3c8%2BMFx5fYGNaHgP6wLPOhybuwVGCHqBwiKED2Z%2BLmGbb; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDRCVFR[feWj1Vr5u3D]=mk3SLVN4HKm; BD_CK_SAM=1; PSINO=7; BDSVRTM=22; H_PS_PSSID=1456_24566_21100_17001_19898_25177_25144_20928',
    'Host': 'www.baidu.com',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

# lock = threading.Lock()


# 1.发起请求
# 2.解析页面
# 3.返回结果
def spider(url, i, resList):
    # print("request start,url=" + url)
    res = "error"
    try:
        # lock.acquire()
        html = requests.get(url, headers=head)
        content = str(html.content)
        # print(content)

        results = re.findall(r"百度为您找到相关结果约.*?个", content, re.I | re.S | re.M)
        for result in results:
            res = result.replace("百度为您找到相关结果约", "").replace("个", "")
    except Exception, e:
        res = "error"
    finally:
        # print("已完成：" + str(i) + ",res=" + res)
        resList[i] = res
        # lock.release()


# 2006-2016
times = ["1136044800", "1167580800", "1199116800", "1230739200", "1262275200", "1293811200", "1325347200",
         "1356969600",
         "1388505600", "1420041600", "1451577600", "1483200000"]

# 已完成爬虫关键词数量
finished = 0

# 表格数据初始写入行数
row = 1
print("开始查询关键词")

# 爬虫数据存储文件
filename = "key word cleaning - " + str(int(time.time())) + ".xls"
w = Workbook()
ws = w.add_sheet("sheet1")

# 写入表头
ws.write(0, 0, "key word")
for i in range(11):
    ws.write(0, i + 1, str(2006 + i))

# 按行读取关键字
for word in open("keyword.txt"):

    # 初始化结果列表 默认查询次数为0
    resList = []
    for k in range(11):
        resList.append("0")
    threads = []

    # 根据关键字 + 时间拼接URL
    for i in range(len(times) - 1):
        startAt = times[i]
        endAt = times[i + 1]
        url = "https://www.baidu.com/s?ie=utf-8&newi=1&mod=1&isbd=1&isid=b657000e00003a48&wd=" + urllib.quote(
            word) + "&rsv_spt=1&rsv_iqid=0xfdcdc2ea00070963&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&oq=%25E7%258E%258B%25E7%259F%25B3%2520%25E4%25B8%2587%25E7%25A7%2591&rsv_t=61751ob5fyLcrE%2BMe%2FeoBRbyPdcXlohG%2Fb1FtOC%2FcgXiaItEJ67kZcVo46gzmJ89VEQk&rsv_pq=e9ef507800040f87&" \
                    "gpc=stf%3D" + startAt + "%2C" + endAt + "%7Cstftype%3D2&tfflag=1&bs=%E7%8E%8B%E7%9F%B3%20%E4%B8%87%E7%A7%91&rsv_sid=1456_24566_21100_17001_19898_25177_25144_20928&_ss=1&clist=49930edbc327db32&hsug&f4s=1&csor=5&_cr1=42497"
        threads.append(threading.Thread(target=spider, args=(url, i, resList)))
        # resList.append(spider(url, i, resList))

    for thread in threads:
        thread.setDaemon(True)
        time.sleep(0.05)
        thread.start()

    for thread in threads:
        thread.join()

    print(resList)

    # 写入表格
    ws.write(row, 0, word.decode('utf8'))
    for i in range(len(resList)):
        ws.write(row, i + 1, str(resList[i]))
    w.save(filename)

    finished = finished + 1
    row = row + 1
    print("已完成" + str(finished) + "个关键词查询，当前完成关键词:" + word)
    # break
print(" 查询完成")
