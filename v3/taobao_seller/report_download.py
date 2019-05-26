# _*_coding:utf-8_*_

import os
import time

import requests

head = {
    "Accept": "*/*",
    # "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Content-Type": "charset=UTF-8",
    "Host": "sycm.taobao.com",
    "Referer": "https://sycm.taobao.com/cc/macroscopic_monitor?spm=a21ag.8718589.TopMenu.d1800.33db50a5HgzquP",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.328.186 Safari/537.36",
    # 操作cookie
    "Cookie": 'miid=2058885027109142822; cna=IbI5EQppkA0CAXUdeMVF2xF8; tg=0; t=4a556d31cbf361ffce8ab5adc6988a0e; thw=cn; enc=LedPnuwzmWJowVYputrLImh%2F8G3HTmuRgzQ9EnoOgdMflGVb803vc%2FG4OwEPYFZ7vBqXckGelmhwYY8rqAK1Ew%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; _cc_=W5iHLLyFfA%3D%3D; UM_distinctid=1697ca2ed9d131-091587565a5daa-10316653-13c680-1697ca2ed9eb21; cookie2=13d06312ab97fe3efaffbb50098d0b99; _tb_token_=38a337ee6e53e; x=2047143080; _m_h5_tk=abb17ebbd92867de47b7420d673a84c3_1558874205165; _m_h5_tk_enc=7c0f1dc45fc662098d8b6b1d244b1b81; JSESSIONID=E3039FC8D4C711441533C6C6B83C974F; mt=ci=0_0; uc3=id2=&nk2=&lg2=; skt=eef56b786b635983; sn=%E5%90%88%E7%BE%8E%E5%AF%8C%E5%85%B4%E6%95%B0%E7%A0%81%E4%B8%93%E8%90%A5%E5%BA%97%3A%E6%98%9F%E6%B5%B7; unb=2200767823914; tracknick=; csg=124c11bf; v=0; uc1=cookie14=UoTZ7H0wHXZi5w%3D%3D&lng=zh_CN; _euacm_ac_l_uid_=2200767823914; 2200767823914_euacm_ac_c_uid_=2047143080; 2200767823914_euacm_ac_rs_uid_=2047143080; _euacm_ac_c_uid_=2047143080; _euacm_ac_rs_uid_=2047143080; _euacm_ac_v_md_=s; _euacm_ac_rs_sid_=109870997; _portal_version_=new; cc_gray=1; miniDialog=true; isg=BJSUVMnStK0xWSBhRIHHl3IYZdTGRbnSvBUyyy53U5vFGTBjV_lzZ_nbGVEk4fAv; l=bBriCWkmv7KYMPJLBOfZZuI8Ly79WQAfGsPzw4OMaIB1ts6a5Koj2HwdzYSXT3Q_E_5hOeKrS2XXmRhJy8aLSx1..'
}

report_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
if not os.path.exists(report_date):
    os.mkdir(report_date)


def download_bussiness_staff():
    yesterday = time.strftime('%Y-%m-%d', time.localtime(time.time() - 86400))

    url = "https://sycm.taobao.com/cc/cockpit/marcro/item/excel/top.json?spm=a21ag.12100459.0.0.273e50a5uwiG4K&dateRange=" + yesterday + "%7C" + yesterday + "&dateType=day&pageSize=10&page=1&order=desc&orderBy=payAmt&dtUpdateTime=false&keyword=&follow=false&cateId=&cateLevel=&guideCateId=&device=0&indexCode=itmUv%2CitemCartCnt%2CpayItmCnt%2CpayAmt%2CpayRate"
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=head)

        business_staff_file = open(report_date + '/【生意参谋平台】商品_所有终端_' + yesterday + '_' + yesterday + '.xls', 'wb')
        for chunk in r.iter_content(100000):
            business_staff_file.write(chunk)
        business_staff_file.close()

    except Exception as e:
        print("请求下载文件出现异常!", e)


def download_shop_total():
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    url = 'https://sycm.taobao.com/adm/v2/downloadById.do?spm=a21ag.10575379.0.0.33c5410cJnnBmY&id=718382&reportType=1'
    try:
        # 发起请求,得到响应结果
        r = requests.get(url, headers=head)

        total_file = open(report_date + '/店铺总体_' + today + '.xls', 'wb')
        for chunk in r.iter_content(100000):
            total_file.write(chunk)
        total_file.close()

    except Exception as e:
        print("请求下载文件出现异常!", e)


def download_popularize():
    today = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    url = 'https://download-subway.simba.taobao.com/download.do?spm=a2e2i.11816827.0.0.10c86abbb8D0lE&custId=1109303120&taskId=7988977&token=bf58975b'
    try:
        # 发起请求,得到响应结果
        head["Host"] = "download-subway.simba.taobao.com"
        r = requests.get(url, headers=head)

        total_file = open(report_date + '/推广报表_' + today + '.zip', 'wb')
        for chunk in r.iter_content(100000):
            total_file.write(chunk)
        total_file.close()

    except Exception as e:
        print("请求下载文件出现异常!", e)


if __name__ == '__main__':
    print("下载生意参谋->品类...")
    download_bussiness_staff()

    print("下载取数->我的报表...")
    download_shop_total()

    print("下载营销推广中心->我的报表...")
    download_popularize()

    print("已完成所有报表获取")
