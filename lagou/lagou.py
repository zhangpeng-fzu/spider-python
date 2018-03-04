# -*-coding:utf-8-*-

import sys
import time
import xlwt
import requests

# 获取公司请求的http头部数据
head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Length": "23",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "JSESSIONID=ABAAABAACEBACDG8DC295FFECEA6F92A56C1FA62F27C86D; user_trace_token=20180225213201-cce120ac-e264-4b04-a42b-e79c6c2ac931; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519565523; _ga=GA1.2.81479230.1519565523; _gid=GA1.2.540394892.1519565523; _gat=1; LGSID=20180225213202-43734294-1a30-11e8-b092-5254005c3644; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fjobs%2Flist_%3Fcity%3D%25E4%25B8%258A%25E6%25B5%25B7%26cl%3Dfalse%26fromSearch%3Dtrue%26labelWords%3D%26suginput%3D; LGUID=20180225213202-437344b5-1a30-11e8-b092-5254005c3644; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1519565529; LGRID=20180225213209-4762a5ac-1a30-11e8-b092-5254005c3644; SEARCH_ID=36fcc398f23049dabed41e8ab9d561e7",
    "Host": "www.lagou.com",
    "Origin": "https://www.lagou.com",
    "Referer": "https://www.lagou.com/jobs/list_java?city=%E4%B8%8A%E6%B5%B7&cl=false&fromSearch=true&labelWords=&suginput=",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "X-Anit-Forge-Code": "0",
    "X-Anit-Forge-Token": "None",
    "X-Requested-With": "XMLHttpRequest"
}


# 通过关键词获取公司列表信息
def get_company_info(keyword):
    url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false&isSchoolJob=0"
    form_data = {
        "first": "true",
        "pn": "1",
        "kd": keyword
    }
    result = []
    # 分页获取,默认设置30页
    for page in range(30):
        print("正在获取第%s页数据" % (page + 1))
        form_data["pn"] = str(page + 1)
        if page > 1:
            form_data["first"] = "false"
        try:
            # 发起请求,得到响应结果
            r = requests.post(url, data=form_data, headers=head)
            response_json = r.json()

            # 解析结果,并汇总到result数组中等待写入表格
            result = result + response_json["content"]["positionResult"]["result"]
        except Exception as e:
            print(e)
        # 休息0.1s,防止触发网站反爬虫
        time.sleep(0.1)
    return result


def write_to_excel(filename, company_infos):
    w = xlwt.Workbook()
    ws = w.add_sheet("sheet1")
    # 写入表头
    excel_header = ["positionId", "companyFullName", "companyLabelList", "district", "education",
                    "firstType", "formatCreateTime", "positionName", "salary", "workYear"]
    for i in range(len(excel_header)):
        ws.write(0, i, excel_header[i])

    row = 1
    for company_info in company_infos:
        for k in range(len(excel_header)):
            try:
                ws.write(row, k, company_info[excel_header[k]])
            except Exception as e:
                print(e)
        row = row + 1
    w.save(filename)


# 主程序
if __name__ == '__main__':

    # 待爬取的关键字
    keywords = ["java", "数据挖掘", "Python", "web前端", "Android"]
    for keyword in keywords:

        # 爬虫数据存储文件名
        filename = keyword + "-" + str(int(time.time())) + ".xls"

        print("开始获取关键字[%s]的数据" % keyword)
        # 获取公司信息
        company_infos = get_company_info(keyword)
        if len(company_infos) > 0:
            print("正在将数据写入表格")
            write_to_excel(filename, company_infos)
            company_infos = []
            print("数据写入表格成功，文件名为%s" % filename)
        else:
            print("根据该关键字未获取到数据")
        time.sleep(1)
