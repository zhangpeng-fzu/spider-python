# -*-coding:utf-8-*-


import requests
from bs4 import BeautifulSoup
import xlwt
import re


def get_year_url(url):
    try:
        # 发起请求,得到响应结果
        r = requests.get(url)

        if r.status_code != 200:
            return
        response_text = str(r.content, "utf-8")
        soup = BeautifulSoup(response_text, features='html.parser')
        l1 = soup.find("a", text=re.compile("行业")).attrs["href"]
        l2 = soup.find("a", text=re.compile("500强排行榜")).attrs["href"]

        return ["http://www.fortunechina.com/fortune500/" + l1, "http://www.fortunechina.com/fortune500/" + l2]

    except Exception as e:
        print(e)


def get_url():
    url_map = {
        "世界": "http://www.fortunechina.com/fortune500/index.htm",
        "美国": "http://www.fortunechina.com/fortune500/node_67.htm",
        "中国": "http://www.fortunechina.com/fortune500/node_4302.htm"
    }
    for k in url_map:
        url = url_map[k]
        try:
            # 发起请求,得到响应结果
            r = requests.get(url)

            if r.status_code != 200:
                return
            response_text = str(r.content, "utf-8")
            soup = BeautifulSoup(response_text, features='html.parser')
            years = soup.findAll("a", text=re.compile("^2.*年$"))
            url_map[k] = {}
            for year in years:
                url_map[k][year.text.replace("年", "")] = get_year_url(
                    "http://www.fortunechina.com/fortune500/" + year.attrs["href"])
        except Exception as e:
            print(e)
    return url_map


def get_company_catogory(url):
    category_map = {}
    try:
        # 发起请求,得到响应结果
        r = requests.get(url)

        if r.status_code != 200:
            return
        response_text = str(r.content, "utf-8")
        soup = BeautifulSoup(response_text, features='html.parser')
        category_name = ""
        lines = soup.findAll("tr")
        for line in lines:
            if line.find("td") and "公司）" in line.find("td").text:
                category_name = line.find("td").text.split(" ")[1].split("（")[0]
            else:
                if len(line.findAll("td")) > 1:
                    company_name = line.findAll("td")[1].text
                    category_map[company_name] = category_name
    except Exception as e:
        print(e)
    return category_map


def get_company(categories_map, url, c, y):
    # 发起请求,得到响应结果
    r = requests.get(url)

    if r.status_code != 200:
        return
    response_text = str(r.content, "utf-8")
    soup = BeautifulSoup(response_text, features='html.parser')

    lines = soup.findAll("tr")

    write_book = xlwt.Workbook()
    data_sheet = write_book.add_sheet('500强')

    excel_head = ["排名", "公司名称", "营业收入", "利润", "资产", "行业分类"]
    for i in range(len(excel_head)):
        data_sheet.write(0, i, excel_head[i])
    try:
        for i in range(500):
            line = lines[i + 1]
            tds = line.findAll("td")
            data_sheet.write(i + 1, 0, tds[0].text)
            data_sheet.write(i + 1, 1, tds[1].text)
            data_sheet.write(i + 1, 2, tds[3].text)
            data_sheet.write(i + 1, 3, tds[4].text)
            data_sheet.write(i + 1, 4, tds[5].text)
            data_sheet.write(i + 1, 5, categories_map[tds[1].text] if tds[1].text in categories_map else "未知分类")

    except Exception as e:
        print(e)
    write_book.save("%s%s年500强.xls" % (c, y))


if __name__ == '__main__':
    urls = get_url()
    print(urls)
    for c in urls:
        for y in urls[c]:
            links = urls[c][y]
            get_company(get_company_catogory(links[0]), links[1], c, y)
