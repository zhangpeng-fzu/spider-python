# -*-coding:utf-8-*-

import time
from xlutils.copy import copy
import xlrd
import requests
import re

# 获取公司请求的http头部数据
head = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
"Connection": "keep-alive",
    # "Content-Length": "499",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "Hm_lvt_c30cfe64c111172dcd13abe3d7532080=1519997376; SSOTOKEN=beacon!2395747A0E6290A7C016D16F63FDA1717FD64F7A7BFDD387D0C63EC8B997E0D07E069C0F275A4283C5A644447617E9B36C95450E6212CFEA437974484BB365A6; Hm_lpvt_c30cfe64c111172dcd13abe3d7532080=1519997537; JSESSIONID=3DED0C4CC0CAA1D4125D54C5B7143F61",
    "Host": "so.iptrm.com",
    "Origin": "http://so.iptrm.com",
    "Referer": "http://so.iptrm.com/app/patentlist",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
}


# 通过获取专利授权数量
def get_patent_authorization_num(year, city):
    url = "http://so.iptrm.com/txnOneCategoryIndex.ajax"
    form_data = {
        "select-key:categoryWords": "pdb;lsscn",
        "select-key:express": "(公开（公告）日 =  ( " + year + " ) ) AND (第一申请人地址 =  ( " + city + " ) )",
        "select-key:express2": "",
        "select-key:categoryIndex": "",
        "select-key:patentLib": "pdb = 'CNB0' OR pdb = 'CNY0' OR pdb = 'CNS0'",
        "select-key:patentType": "patent2",
        "select-key:categoryNum": "5",
        "select-key:categoryStart": "0"
    }

    try:
        # 发起请求,得到响应结果
        r = requests.post(url, data=form_data, headers=head)

        if r.status_code != 200:
            print("获取专利授权数据失败")
            return
        response_text = str(r.content).replace("\\n", "")
        CNY0, CNB0, CNS0 = "", "", ""
        results = re.findall(r"CNY0<.*?</value", response_text, re.I | re.S | re.M)
        for result in results:
            CNY0 = result.replace("CNY0</key><value>", "").replace("</value", "")
            break

        results = re.findall(r"CNB0<.*?</value", response_text, re.I | re.S | re.M)
        for result in results:
            CNB0 = result.replace("CNB0</key><value>", "").replace("</value", "")
            break

        results = re.findall(r"CNS0<.*?</value", response_text, re.I | re.S | re.M)
        for result in results:
            CNS0 = result.replace("CNS0</key><value>", "").replace("</value", "")
            break

        return [CNB0, CNY0, CNS0]

    except Exception as e:
        print(e)
    finally:
        time.sleep(0.1)


# 通过获取专利授权数量
def get_patent_apply_num(year, city):
    url = "http://so.iptrm.com/txnOneCategoryIndex.ajax"
    form_data = {
        "select-key:categoryWords": "pdb;lsscn",
        "select-key:express": "(申请日 =  ( " + year + " ) ) AND (第一申请人地址 =  ( " + city + " ) )",
        "select-key:express2": "",
        "select-key:categoryIndex": "",
        "select-key:patentLib": "pdb = 'CNA0' OR pdb = 'CNY0' OR pdb = 'CNS0'",
        "select-key:patentType": "patent2",
        "select-key:categoryNum": "5",
        "select-key:categoryStart": "0"
    }

    try:
        # 发起请求,得到响应结果
        r = requests.post(url, data=form_data, headers=head)

        if r.status_code != 200:
            print("获取专利申请数据失败")
            return
        response_text = str(r.content).replace("\\n", "")
        CNY0, CNA0, CNS0 = "", "", ""
        results = re.findall(r"CNY0<.*?</value", response_text, re.I | re.S | re.M)
        for result in results:
            CNY0 = result.replace("CNY0</key><value>", "").replace("</value", "")
            break

        results = re.findall(r"CNA0<.*?</value", response_text, re.I | re.S | re.M)
        for result in results:
            CNA0 = result.replace("CNA0</key><value>", "").replace("</value", "")
            break

        results = re.findall(r"CNS0<.*?</value", response_text, re.I | re.S | re.M)
        for result in results:
            CNS0 = result.replace("CNS0</key><value>", "").replace("</value", "")
            break

        return [CNA0, CNY0, CNS0]

    except Exception as e:
        print(e)
    finally:
        time.sleep(0.1)


# 主程序
if __name__ == '__main__':
    wWorkbook = xlrd.open_workbook('264个地级市.xls')
    mySheet = wWorkbook.sheet_by_index(0)
    wb = copy(wWorkbook)

    years = ["2012", "2014", "2016"]
    for i in range(316):
        city = str(mySheet.cell_value(i, 0)).strip()
        citydata = []
        if "市" in city:
            print("正在获取【%s】" % city)
            for year in years:
                citydata = citydata + get_patent_authorization_num(year, city)
                citydata = citydata + get_patent_apply_num(year, city)
        else:
            continue
        for k in range(len(citydata)):
            # 通过get_sheet()获取的sheet有write()方法
            ws = wb.get_sheet(0)
            ws.write(i, k + 1, citydata[k])

        wb.save('264个地级市.xls')
