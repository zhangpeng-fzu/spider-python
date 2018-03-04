# -*-coding:utf8-*-

import sys
import json
import time
import ConfigParser
import re
import requests
from pyExcelerator import *

reload(sys)

sys.setdefaultencoding('utf-8')

cf = ConfigParser.ConfigParser()
cf.read("application.conf")
head = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_uab_collina=151239518894710624316078; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAFiUlEQVRYR8WWeWxUVRTGf2damLIJAjGmhbIEJcrSUDoFROiMJiKKCRg1iohsYmUxgAYQDKUgKhBNq0D4AyG4ICqGBAVZlJkCssy0xig7SJVVoFTLoiW0c8yZeVPaytKaqjeZzMu75953vvN937lXUFWcMXzZMlofO8asGTNir1CRjkAAaCUQrpio4YNCJtBaYHoNl1wzLKc4pyLPawVIZSBjFi0i6cQJps%2BZUxlIZ2CTk0x5bZNRGAM0F3itpmsVGgtcrBxfKyCZixfTc%2BdOxi5ciPvyZcri4ylp2rQP8B5wN9ADmAS8CjQDXgayBPbYx4E3gC5OAtMEtiuMcNavBJ4EhgksVxBgPPCoE%2F%2BZwEIFK9w3wDJgCvAJMCS3OOfKjQpRhZERS5eSlZ3NwrFjK9bMnTJlMdAd6EVUWiFgssBmhclAAeAHfgBGAbuAj4FFAlscRpJMWgom0%2F0O2EeAMoH5CkOAu5wYK1Q20BX4DThsRcwtzjldYyAmrZZFRdU9cieQZ9JygFjSM5wkXwT2AEFgK5BqPlIYBtwmMK8aEGPBqm0yMyMOFPhdwb7xPnAPkABsd4pnhVsDjKwVEDN78tGjZGdlVfZIJ%2BBzwP7NcMbIOIGdCpWBHHMawkWFD4GDArMcIC2dZwNi663qbwPPCxQoPA7Mcr4RD2wE7ncKZ0CG5hbnFNeIkY4HDrBg3DjqXbnC4BUrOJmYGPFJaULCBOBNYIDTvaySPuBLYC5QCJiPTA73ObKaBpQCHqAv8Lrzb%2Buedipv3ljurDNv2XiKqHeWAj2BS0A%2B8ExucY4Buu6o8Ei7wsIIiLjyci673Rxp3z4GJAU4b50H2A24gH6AMXAKaOKAKXMSvwzsdaRhkksC6jm%2BsH3yYm1coyy3BLY58eafNsCfgHVI%2B7mB%2BNziHNvz5kCuHyFWoTobui0%2FWe5NO3q9DTUvv4tkpP1Yfb5W7feam8vfgVgylIW%2FBukQYUX5SnyeURoIbQA1SZSBa6Z4096N7al5oemEdTxCCcjP4vUYq1e9mBfqhup6kF9BG6CNUsXXqeIsMSAdSlrQ%2F2hH1icf4FDTc1XSrdJ%2BawrE4tRfmICctfa4W7zp5oXIUH%2FwOMRliq%2B7eSj6Lj%2B%2FKRf0BOLqj57fgTQ%2Bg8o08aVZa4%2FGBEKHrEOJ1%2FOSBoIhkOPi9QyKzYf2rNZuRYnEqYt1bfbXHZBo0qFVCIOMBfGmh9Qfegx0AVxqJT6feSaapLGhOpMGerv06HFOA8HtICpeT29n3tgIonGDrAAayM%2BG8AT0UovYPl8UfqAnGpfw7P5U%2FElHONisqG4YiSSwtaA7ZeW7EFkhXs9QDYTWolwQn8dO8KuyCYTmoYyhYbjNVSC0EG%2B6HZBoIN%2BHhjfhcj0kGWkbNS84mzCvUN%2BdKL1TzliMSSsu7OK5fR42J%2F1Ut0AcSewDTbTqIY1%2FAR1o7FQDsg7oLF5PcnRNcEfk%2FlUBJDQR1fm49A7J6FEYAaJMjTH4XwGZCLwFugSkl3g9sbvWVUaqVTgqrUqMxJh1MVgy0j%2F9f4BETF9kZ0pL0CzxptsJXWWov2AAUr6aeu4kk4r6g98jUoDKfOKlEWXN90Qah8pw8XlWqj%2BYA%2FIgXOxMXJN%2B0jdtrUlLFEbvTWdj68MU3lL1oP%2FHXauqdIIfAU%2FEEq0OpJKcEhAJoDqCBtqeP1wbEE0xCVEaNxUNjwZXNuhsXAwlHLlt2w374dyu367rc7ItqUVJnGp4gTXt9lIaV9FPqBsgW79LIVyeKRmeF64FoqJ7BULvgLajnntkhJlAcDi42oo3LXK500D%2BJDT8AMgS8XlW6ZZQb8I6GG00JTdl04XUs4mRy547HM%2FeW09zvr5dIqKjToDcKPm6mvtXTva6Sq42%2B9wMyF8lwJ4360rHjAAAAABJRU5ErkJggg%3D%3D%2CMacIntel.1440.900.24; UM_distinctid=16021c732748a-038f1afe030b48-17386d57-13c680-16021c732795b9; _ga=GA1.2.963593815.1512395190; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1512396030805; __asc=891fb65516021c7336d09152839; __auc=891fb65516021c7336d09152839; sid=cKTXpbOmv6CWe4U3kAlGqCQw4Ip.R36mOZeHcOHZCzIptOlrRLv4pIBMGLjb7jBTIGrsKC0; CNZZDATA1256903590=1745790908-1512393901-%7C1512393901',
    'Host': 'cn.investing.com',
    'Pragma': 'no-cache',
    'Referer': 'https://cn.investing.com/currencies/usd-cny-chart',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Request': 'json',
    'X-Requested-With': 'XMLHttpRequest'
}


# 获取随机ID
def get_random_id(url):
    try:
        head['Host'] = 'cn.investing.com'
        html = requests.get(url, headers=head)
        content = str(html.content)

        res = {}

        results = re.findall(r"carrier=.*?&time", content, re.I | re.S | re.M)
        for result in results:
            res["random_id"] = result.replace("carrier=", "").replace("&time", "")
            break
        results = re.findall(r"pair_ID=.*?&", content, re.I | re.S | re.M)
        for result in results:
            res["symbol"] = result.replace("pair_ID=", "").replace("&", "")
            break
        return res
    except Exception, e:
        print e


# 获取历史数据
def get_history(random_id, symbol, resolution, start_timestamp, end_timestamp):
    history_data = {"t": [], "c": [], "s": 'ok'}

    # 分段获取
    while start_timestamp < end_timestamp:
        try:
            history_url = "https://tvc4.forexpros.com/%s/%s/6/6/28/history?symbol=%s&resolution=%s&from=%s&to=%s" % (
                random_id, int(time.time()), symbol, resolution, start_timestamp, end_timestamp)
            head['Host'] = 'tvc4.forexpros.com'
            html = requests.get(history_url, headers=head)
            content = str(html.content)
            temp_data = json.loads(content)

            if temp_data['s'] == 'no_data':
                break

            history_data['t'] = history_data['t'] + temp_data['t']
            history_data['c'] = history_data['c'] + temp_data['c']

            last_timestamp = history_data['t'][-1]

            start_timestamp = int(last_timestamp) + get_interval_by_resolution(resolution) * 60
        except Exception, e:
            print e
            return history_data

    if len(history_data['t']) == 0:
        history_data['s'] = 'no_data'
    else:
        history_data['s'] = 'ok'
    return history_data


# 数据写入表格
def write_file(filename, data):
    t = data['t']
    c = data['c']
    w = Workbook()
    ws = w.add_sheet("sheet1")
    ws.write(0, 0, "时间".decode('utf8'))
    ws.write(0, 1, "价格".decode('utf8'))
    row = 1
    for i in range(len(t)):
        try:
            ws.write(row, 0, time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t[i])))
            ws.write(row, 1, str(c[i]))
        except Exception, e:
            print e
        row = row + 1

    w.save(filename)


def get_interval_by_resolution(resolution):
    interval = resolution
    if resolution == "D":
        interval = 24 * 60
    elif resolution == "W":
        interval = 7 * 24 * 60
    elif resolution == "M":
        interval = 30 * 7 * 24 * 60
    return int(interval)


def check_config(currency_list, start_timestamp, end_timestamp, resolution):
    if len(currency_list) == 0 or currency_list[0] == '':
        print "请选择货币类型"
        sys.exit()

    if end_timestamp <= start_timestamp:
        print "结束时间必须大于开始时间"
        sys.exit()

    if resolution == '1' and end_timestamp - start_timestamp > 60 * 60 * 24 * 180:
        print "数据频率为1分钟时，时间区间不能超过半年"
        sys.exit()

    if resolution == '5' and end_timestamp - start_timestamp > 60 * 60 * 24 * 365 * 2:
        print "数据频率为5分钟时，时间区间不能超过两年"
        sys.exit()


def complete_history_data(currency_data, start_timestamp, end_timestamp):
    first_timestamp = int(currency_data['t'][0])
    last_timestamp = int(currency_data['t'][-1])
    head_list = {"t": [], "c": [], "s": 'ok'}
    tail_list = {"t": [], "c": [], "s": 'ok'}

    if first_timestamp > start_timestamp:
        i = 0
        while first_timestamp > start_timestamp:
            head_list['t'].append(start_timestamp)
            head_list['c'].append('0')
            i = i + 1
            start_timestamp = int(start_timestamp) + get_interval_by_resolution(resolution) * 60

    if last_timestamp < end_timestamp:
        tail_list = {"t": [], "c": [], "s": 'ok'}
        i = 0
        while last_timestamp <= end_timestamp:
            last_timestamp = int(last_timestamp) + get_interval_by_resolution(resolution) * 60
            tail_list['t'].append(last_timestamp)
            tail_list['c'].append('0')
            i = i + 1
    currency_data['t'] = head_list['t'] + currency_data['t'] + tail_list['t']
    currency_data['c'] = head_list['c'] + currency_data['c'] + tail_list['c']
    return currency_data


print "开始读取配置文件"
start = cf.get("inversting", "start")
end = cf.get("inversting", "end")
currencies = cf.get("inversting", "currencies")
resolution = cf.get("inversting", "resolution")

currency_list = currencies.split(",")

# 转换时间格式
start_timestamp = int(time.mktime(time.strptime(start, "%Y-%m-%d %H:%M:%S")))
end_timestamp = int(time.mktime(time.strptime(end, "%Y-%m-%d %H:%M:%S")))

check_config(currency_list, start_timestamp, end_timestamp, resolution)

for currency in currency_list:
    try:
        print "============================="
        print "开始获取数据，货币类型：%s,时间区间:%s-%s,数据频率：%s" % (currency, start, end, resolution)
        filename = "%s_%s_%s.xls" % (
            currency.replace("/", "_"), start.split(" ")[0].replace("-", ""), end.split(" ")[0].replace("-", ""))

        res = get_random_id("https://cn.investing.com/currencies/%s-chart" % (currency.replace("/", "-").lower()))
        if len(res) is None:
            print "获取随机ID失败"
            continue

        currency_data = get_history(res['random_id'], res['symbol'], resolution, start_timestamp, end_timestamp)
        if currency_data['s'] == "no_data":
            print "该时间段没有数据"
            continue
        currency_data = complete_history_data(currency_data, start_timestamp, end_timestamp)

        write_file("result/" + filename, data=currency_data)

        print "数据获取完成，文件名：" + filename
    except Exception, e:
        print e

print "所有数据获取完成"
