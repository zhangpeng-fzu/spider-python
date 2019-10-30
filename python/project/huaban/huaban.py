# -*-coding:utf8-*-

import sys
import json
import time
import urllib
import os
import requests

reload(sys)

sys.setdefaultencoding('utf-8')

head = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_uab_collina=151239518894710624316078; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAFiUlEQVRYR8WWeWxUVRTGf2damLIJAjGmhbIEJcrSUDoFROiMJiKKCRg1iohsYmUxgAYQDKUgKhBNq0D4AyG4ICqGBAVZlJkCssy0xig7SJVVoFTLoiW0c8yZeVPaytKaqjeZzMu75953vvN937lXUFWcMXzZMlofO8asGTNir1CRjkAAaCUQrpio4YNCJtBaYHoNl1wzLKc4pyLPawVIZSBjFi0i6cQJps%2BZUxlIZ2CTk0x5bZNRGAM0F3itpmsVGgtcrBxfKyCZixfTc%2BdOxi5ciPvyZcri4ylp2rQP8B5wN9ADmAS8CjQDXgayBPbYx4E3gC5OAtMEtiuMcNavBJ4EhgksVxBgPPCoE%2F%2BZwEIFK9w3wDJgCvAJMCS3OOfKjQpRhZERS5eSlZ3NwrFjK9bMnTJlMdAd6EVUWiFgssBmhclAAeAHfgBGAbuAj4FFAlscRpJMWgom0%2F0O2EeAMoH5CkOAu5wYK1Q20BX4DThsRcwtzjldYyAmrZZFRdU9cieQZ9JygFjSM5wkXwT2AEFgK5BqPlIYBtwmMK8aEGPBqm0yMyMOFPhdwb7xPnAPkABsd4pnhVsDjKwVEDN78tGjZGdlVfZIJ%2BBzwP7NcMbIOIGdCpWBHHMawkWFD4GDArMcIC2dZwNi663qbwPPCxQoPA7Mcr4RD2wE7ncKZ0CG5hbnFNeIkY4HDrBg3DjqXbnC4BUrOJmYGPFJaULCBOBNYIDTvaySPuBLYC5QCJiPTA73ObKaBpQCHqAv8Lrzb%2Buedipv3ljurDNv2XiKqHeWAj2BS0A%2B8ExucY4Buu6o8Ei7wsIIiLjyci673Rxp3z4GJAU4b50H2A24gH6AMXAKaOKAKXMSvwzsdaRhkksC6jm%2BsH3yYm1coyy3BLY58eafNsCfgHVI%2B7mB%2BNziHNvz5kCuHyFWoTobui0%2FWe5NO3q9DTUvv4tkpP1Yfb5W7feam8vfgVgylIW%2FBukQYUX5SnyeURoIbQA1SZSBa6Z4096N7al5oemEdTxCCcjP4vUYq1e9mBfqhup6kF9BG6CNUsXXqeIsMSAdSlrQ%2F2hH1icf4FDTc1XSrdJ%2BawrE4tRfmICctfa4W7zp5oXIUH%2FwOMRliq%2B7eSj6Lj%2B%2FKRf0BOLqj57fgTQ%2Bg8o08aVZa4%2FGBEKHrEOJ1%2FOSBoIhkOPi9QyKzYf2rNZuRYnEqYt1bfbXHZBo0qFVCIOMBfGmh9Qfegx0AVxqJT6feSaapLGhOpMGerv06HFOA8HtICpeT29n3tgIonGDrAAayM%2BG8AT0UovYPl8UfqAnGpfw7P5U%2FElHONisqG4YiSSwtaA7ZeW7EFkhXs9QDYTWolwQn8dO8KuyCYTmoYyhYbjNVSC0EG%2B6HZBoIN%2BHhjfhcj0kGWkbNS84mzCvUN%2BdKL1TzliMSSsu7OK5fR42J%2F1Ut0AcSewDTbTqIY1%2FAR1o7FQDsg7oLF5PcnRNcEfk%2FlUBJDQR1fm49A7J6FEYAaJMjTH4XwGZCLwFugSkl3g9sbvWVUaqVTgqrUqMxJh1MVgy0j%2F9f4BETF9kZ0pL0CzxptsJXWWov2AAUr6aeu4kk4r6g98jUoDKfOKlEWXN90Qah8pw8XlWqj%2BYA%2FIgXOxMXJN%2B0jdtrUlLFEbvTWdj68MU3lL1oP%2FHXauqdIIfAU%2FEEq0OpJKcEhAJoDqCBtqeP1wbEE0xCVEaNxUNjwZXNuhsXAwlHLlt2w374dyu367rc7ItqUVJnGp4gTXt9lIaV9FPqBsgW79LIVyeKRmeF64FoqJ7BULvgLajnntkhJlAcDi42oo3LXK500D%2BJDT8AMgS8XlW6ZZQb8I6GG00JTdl04XUs4mRy547HM%2FeW09zvr5dIqKjToDcKPm6mvtXTva6Sq42%2B9wMyF8lwJ4360rHjAAAAABJRU5ErkJggg%3D%3D%2CMacIntel.1440.900.24; UM_distinctid=16021c732748a-038f1afe030b48-17386d57-13c680-16021c732795b9; _ga=GA1.2.963593815.1512395190; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1512396030805; __asc=891fb65516021c7336d09152839; __auc=891fb65516021c7336d09152839; sid=cKTXpbOmv6CWe4U3kAlGqCQw4Ip.R36mOZeHcOHZCzIptOlrRLv4pIBMGLjb7jBTIGrsKC0; CNZZDATA1256903590=1745790908-1512393901-%7C1512393901',
    'Host': 'huaban.com',
    'Pragma': 'no-cache',
    'Referer': 'http://huaban.com/boards/14283600',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Request': 'json',
    'X-Requested-With': 'XMLHttpRequest'
}

# 初始图片id
pin_id = "200000000"

# 每页数目
limit = 100

# 抓取图片总数
count = 0

# 图片存放目录
folder_path = 'images_' + str(int(time.time()))
os.mkdir(folder_path)


# 根据mime获取图片后缀
def get_ext_by_mime(mime):
    if mime == 'image/jpeg':
        return '.jpg'
    if mime == 'image/png':
        return '.png'
    if mime == 'image/bmp':
        return '.bmp'
    if mime == 'image/webp':
        return '.webp'
    if mime == 'image/gif':
        return '.gif'
    return '.jpg'


# 1.发起请求
# 2.解析数据
# 3.下载图片
def spider(url):
    # print("request start,url=" + url)
    global count
    pid = 0
    try:
        html = requests.get(url, headers=head)
        content = str(html.content)
        json_data = json.loads(content)['board']['pins']
        size = len(json_data)
        if size == 0:
            return 0
        for i in range(size):
            key = json_data[i]['file']['key']
            mime = json_data[i]['file']['type']
            ext = get_ext_by_mime(mime)
            filename = key + ext
            print("正在下载图片:" + filename)
            urllib.urlretrieve('http://img.hb.aicdn.com/' + key, folder_path + "/" + filename)
            count = count + 1
            pid = json_data[i]['pin_id']

        return pid
    except Exception as e:
        print(e)
        return 0


# 开始抓取图片
while pin_id > 0:
    pin_id = spider(
        "http://huaban.com/boards/14283600?jas9jokw&max=" + str(pin_id) + "&limit=" + str(limit) + "&wfl=1")
    print("当前pin_id = " + str(pin_id))

print("一共抓取" + str(count) + "张图片")
