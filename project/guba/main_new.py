# -*-coding:utf-8-*-

import xlrd
import xlwt
import requests
import re
import time
import json
from xlrd import xldate_as_tuple
from datetime import datetime

# 获取公司请求的http头部数据
header = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Host": "api.so.eastmoney.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/82.0.4068.5 Safari/537.36"
}

write_book = xlwt.Workbook()  # 打开excel
data_sheet = write_book.add_sheet('数据')
total_company_num = 134


# 发送获取列表请求
def send(url, retry=0):
    if retry > 3:
        return None
    header["Host"] = "guba.eastmoney.com"
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=header)

        if r.status_code != 200:
            print("获取数据失败")
            return
        # 解析页数
        page_arr = str(re.findall(r"data-pager.*?>", str(r.content), re.I | re.S | re.M)[0]).split("|")
        total = int(page_arr[1])
        size = int(page_arr[2])
        if total % size == 0:
            page = int(total / size)
        else:
            page = int(total / size) + 1

        # 解析帖子信息
        news_arr = re.findall(r"<div class=\"articleh normal_post.*?/div>", str(r.content, "utf-8"), re.I | re.S | re.M)
        news_simple_data = []
        for news in news_arr:
            data_arr = re.findall(r"<span.*?</span>", str(news), re.I | re.S | re.M)

            # 浏览量
            pv = str(data_arr[0]).split(">")[1].split("<")[0]
            if "万" in pv:
                pv = float(pv.replace("万", "")) * 10000
            # 链接
            href = str(data_arr[2]).split("href=")[1].split("title")[0].strip().replace("\"", "")

            # 用户
            try:
                user = str(data_arr[3]).split("<font>")[1].split("</font>")[0].strip().replace("\"", "")
            except Exception as e:
                print(e)
                user = ""
            # 发布时间
            news_date = str(data_arr[4]).split(">")[1].split("<")[0].split(" ")[0]
            news_simple_data.append({
                "pv": pv,
                "href": href,
                "user": user,
                "date": news_date
            })
        # 完善帖子时间
        news_detail = fetch_first_news("http://guba.eastmoney.com" + news_simple_data[0]["href"], 0)
        if news_detail is None:
            news_detail = {
                "push_time": "2019-12"
            }
        year = news_detail["push_time"].split("-")[0]
        month = news_detail["push_time"].split("-")[1]

        for simple_news in news_simple_data:
            news_month = int(simple_news["date"].split("-")[0])
            if int(month) >= news_month:
                simple_news["date"] = year + "-" + simple_news["date"]
            else:
                simple_news["date"] = str(int(year) - 1) + "-" + simple_news["date"]
        return {
            "page": page,
            "data": news_simple_data
        }
    except Exception as e:
        print(e)
        send(url, ++retry)
    finally:
        time.sleep(0.1)


# 读原始表格并解析
def read_xls():
    work_book = xlrd.open_workbook('company.xlsx')
    sheet = work_book.sheet_by_index(0)
    company_arr = []
    for i in range(3, total_company_num):
        info = {"name": str(sheet.cell_value(i, 1)).strip(),
                "code": str(sheet.cell_value(i, 0)).strip()}

        ss_date_arr = xldate_as_tuple(sheet.cell_value(i, 16), 0)
        info["ss_date"] = "2019-" + str(ss_date_arr[1]) + "-" + str(ss_date_arr[2])

        sg_month = str(sheet.cell_value(i, 15)).strip().split(" ")[0].split("-")[0]
        if int(ss_date_arr[1]) < int(sg_month):
            info["sg_date"] = "2018-" + str(sheet.cell_value(i, 15)).strip().split(" ")[0]
        else:
            info["sg_date"] = "2019-" + str(sheet.cell_value(i, 15)).strip().split(" ")[0]

        company_arr.append(info)
    return company_arr


# 写入结果数据
def write_xls(row, company_data):
    data_sheet.write(row, 1, company_data["name"])
    data_sheet.write(row, 2, company_data["sg_total"])
    data_sheet.write(row, 3, company_data["sg_pv"])
    data_sheet.write(row, 4, company_data["ss_total"])
    data_sheet.write(row, 5, company_data["ss_pv"])
    write_book.save('company-data.xls')


# 判断是否7天内
def is_seven_day(start, end):
    # 帖子创建时间
    start_date = datetime.strptime(start, '%Y-%m-%d')
    # 上市或者申购时间
    end_date = datetime.strptime(end, '%Y-%m-%d')

    offset = (end_date - start_date).days
    return 0 <= offset <= 7


# 判断是否超过上市时间
def older_ss_date(start, end):
    # 帖子创建时间
    start_date = datetime.strptime(start, '%Y-%m-%d')
    # 上市或者申购时间
    end_date = datetime.strptime(end, '%Y-%m-%d')

    offset = (start_date - end_date).days
    return offset > 0


# 判断小于申购时间7天
def less_7_sg_date(start, end):
    # 帖子创建时间
    start_date = datetime.strptime(start, '%Y-%m-%d')
    # 上市或者申购时间
    end_date = datetime.strptime(end, '%Y-%m-%d')

    offset = (start_date - end_date).days
    return offset < -7


# 获取第一条帖子发布时间
def fetch_first_news(url, retry_time=0):
    if retry_time > 3:
        return None
    try:
        if "问董秘" in url:
            return None
        header["Host"] = "guba.eastmoney.com"
        r = requests.get(url, headers=header)

        if r.status_code != 200:
            print("获取数据失败")
            return
        content = str(r.content, "utf-8")
        pv = str(re.findall(r"post_click_count.*?,", content, re.I | re.S | re.M)[0]).split(":")[1].split(",")[0]
        push_time = str(re.findall(r"post_publish_time.*?,", content, re.I | re.S | re.M)[0]).split(":")[1].split(" ")[
            0]
        user = str(re.findall(r"user_nickname.*?,", content, re.I | re.S | re.M)[0]).split(":")[1].split(",")[0]
        return {
            "pv": pv,
            "push_time": push_time.replace("\"", ""),
            "user": user,
        }
    except Exception as e:
        print(e)
        fetch_first_news(url, ++retry_time)


# 获取帖子列表及每个帖子访问量数据
def fetch_list(company_info):
    company_code = str(company_info["code"].split(".")[0])
    res_data = {}
    url = "http://guba.eastmoney.com/list,%s,f_%d.html" % (company_code, 1)

    try:
        json_obj = send(url)
        total_page = int(json_obj["page"])
        sg_pv = 0
        ss_pv = 0
        sg_total = 0
        ss_total = 0
        count = 0

        for i in range(total_page, 0, -1):
            # 连续3条时间超过上市时间，停止
            if count >= 3:
                break

            url = "http://guba.eastmoney.com/list,%s,f_%d.html" % (company_code, i)
            json_obj = send(url)
            if json_obj is None or json_obj['data'] is None:
                continue
            print(url)
            news_data = json_obj["data"]
            # 列表第一条时间小于申购时间，则该列表所有帖子时间都小于申购时间
            if less_7_sg_date(news_data[0]["date"], company_info["sg_date"]):
                continue

            # 列表正序
            news_data = sorted(news_data, key=lambda x: x["date"], reverse=False)

            for new_data in news_data:
                # xx资讯的帖子不统计
                if company_info["name"] in new_data["user"]:
                    continue
                create_time = new_data["date"]
                # 超过上市时间,由于是正序排列，后面的数据都会超过上市时间，不再获取
                if older_ss_date(create_time, company_info["ss_date"]):
                    # 避免某页中混入时间错误数据
                    count = count + 1
                    if count >= 3:
                        # 忽略该页剩余
                        break
                    else:
                        # 忽略该条
                        continue
                else:
                    count = 0
                # print(create_time, company_info["sg_date"], company_info["ss_date"])
                # 上市时间前7天
                if is_seven_day(create_time, company_info["ss_date"]):
                    ss_total = ss_total + 1
                    ss_pv = ss_pv + int(new_data["pv"])

                # 申购时间前7天
                if is_seven_day(create_time, company_info["sg_date"]):
                    sg_total = sg_total + 1
                    sg_pv = sg_pv + int(new_data["pv"])

        res_data["name"] = company_info["name"]
        # 上市前7天帖子数量
        res_data["ss_total"] = ss_total
        # 申购前7天帖子数量
        res_data["sg_total"] = sg_total

        res_data["ss_pv"] = ss_pv
        res_data["sg_pv"] = sg_pv
        return res_data

    except Exception as e:
        print(url)
        print(e)
    finally:
        time.sleep(0.1)


if __name__ == '__main__':
    i = 1
    for company in read_xls():
        res = fetch_list(company)
        print(res)
        write_xls(i, res)
        i = i + 1
