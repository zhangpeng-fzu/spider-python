# -*-coding:utf8-*-

import sys
import time
import requests
from pyExcelerator import *
from xml.etree import ElementTree as ET

reload(sys)

sys.setdefaultencoding('utf-8')

head = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '_uab_collina=151239518894710624316078; _f=iVBORw0KGgoAAAANSUhEUgAAADIAAAAUCAYAAADPym6aAAAFiUlEQVRYR8WWeWxUVRTGf2damLIJAjGmhbIEJcrSUDoFROiMJiKKCRg1iohsYmUxgAYQDKUgKhBNq0D4AyG4ICqGBAVZlJkCssy0xig7SJVVoFTLoiW0c8yZeVPaytKaqjeZzMu75953vvN937lXUFWcMXzZMlofO8asGTNir1CRjkAAaCUQrpio4YNCJtBaYHoNl1wzLKc4pyLPawVIZSBjFi0i6cQJps%2BZUxlIZ2CTk0x5bZNRGAM0F3itpmsVGgtcrBxfKyCZixfTc%2BdOxi5ciPvyZcri4ylp2rQP8B5wN9ADmAS8CjQDXgayBPbYx4E3gC5OAtMEtiuMcNavBJ4EhgksVxBgPPCoE%2F%2BZwEIFK9w3wDJgCvAJMCS3OOfKjQpRhZERS5eSlZ3NwrFjK9bMnTJlMdAd6EVUWiFgssBmhclAAeAHfgBGAbuAj4FFAlscRpJMWgom0%2F0O2EeAMoH5CkOAu5wYK1Q20BX4DThsRcwtzjldYyAmrZZFRdU9cieQZ9JygFjSM5wkXwT2AEFgK5BqPlIYBtwmMK8aEGPBqm0yMyMOFPhdwb7xPnAPkABsd4pnhVsDjKwVEDN78tGjZGdlVfZIJ%2BBzwP7NcMbIOIGdCpWBHHMawkWFD4GDArMcIC2dZwNi663qbwPPCxQoPA7Mcr4RD2wE7ncKZ0CG5hbnFNeIkY4HDrBg3DjqXbnC4BUrOJmYGPFJaULCBOBNYIDTvaySPuBLYC5QCJiPTA73ObKaBpQCHqAv8Lrzb%2Buedipv3ljurDNv2XiKqHeWAj2BS0A%2B8ExucY4Buu6o8Ei7wsIIiLjyci673Rxp3z4GJAU4b50H2A24gH6AMXAKaOKAKXMSvwzsdaRhkksC6jm%2BsH3yYm1coyy3BLY58eafNsCfgHVI%2B7mB%2BNziHNvz5kCuHyFWoTobui0%2FWe5NO3q9DTUvv4tkpP1Yfb5W7feam8vfgVgylIW%2FBukQYUX5SnyeURoIbQA1SZSBa6Z4096N7al5oemEdTxCCcjP4vUYq1e9mBfqhup6kF9BG6CNUsXXqeIsMSAdSlrQ%2F2hH1icf4FDTc1XSrdJ%2BawrE4tRfmICctfa4W7zp5oXIUH%2FwOMRliq%2B7eSj6Lj%2B%2FKRf0BOLqj57fgTQ%2Bg8o08aVZa4%2FGBEKHrEOJ1%2FOSBoIhkOPi9QyKzYf2rNZuRYnEqYt1bfbXHZBo0qFVCIOMBfGmh9Qfegx0AVxqJT6feSaapLGhOpMGerv06HFOA8HtICpeT29n3tgIonGDrAAayM%2BG8AT0UovYPl8UfqAnGpfw7P5U%2FElHONisqG4YiSSwtaA7ZeW7EFkhXs9QDYTWolwQn8dO8KuyCYTmoYyhYbjNVSC0EG%2B6HZBoIN%2BHhjfhcj0kGWkbNS84mzCvUN%2BdKL1TzliMSSsu7OK5fR42J%2F1Ut0AcSewDTbTqIY1%2FAR1o7FQDsg7oLF5PcnRNcEfk%2FlUBJDQR1fm49A7J6FEYAaJMjTH4XwGZCLwFugSkl3g9sbvWVUaqVTgqrUqMxJh1MVgy0j%2F9f4BETF9kZ0pL0CzxptsJXWWov2AAUr6aeu4kk4r6g98jUoDKfOKlEWXN90Qah8pw8XlWqj%2BYA%2FIgXOxMXJN%2B0jdtrUlLFEbvTWdj68MU3lL1oP%2FHXauqdIIfAU%2FEEq0OpJKcEhAJoDqCBtqeP1wbEE0xCVEaNxUNjwZXNuhsXAwlHLlt2w374dyu367rc7ItqUVJnGp4gTXt9lIaV9FPqBsgW79LIVyeKRmeF64FoqJ7BULvgLajnntkhJlAcDi42oo3LXK500D%2BJDT8AMgS8XlW6ZZQb8I6GG00JTdl04XUs4mRy547HM%2FeW09zvr5dIqKjToDcKPm6mvtXTva6Sq42%2B9wMyF8lwJ4360rHjAAAAABJRU5ErkJggg%3D%3D%2CMacIntel.1440.900.24; UM_distinctid=16021c732748a-038f1afe030b48-17386d57-13c680-16021c732795b9; _ga=GA1.2.963593815.1512395190; _cnzz_CV1256903590=is-logon%7Clogged-out%7C1512396030805; __asc=891fb65516021c7336d09152839; __auc=891fb65516021c7336d09152839; sid=cKTXpbOmv6CWe4U3kAlGqCQw4Ip.R36mOZeHcOHZCzIptOlrRLv4pIBMGLjb7jBTIGrsKC0; CNZZDATA1256903590=1745790908-1512393901-%7C1512393901',
    'Pragma': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintoshintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Host': 'www.zillow.com',
    'Upgrade-Insecure-Requests': '1'
}


# 通过zpid调用API获取数据
def get_data_by_zpid(url):
    try:
        html = requests.get(url, headers=head)
        return str(html.content)
    except Exception, e:
        print e
        return ""


# 处理返回的xml数据
def xml_2_dict(xml_str):
    result = {
        'zpid': '',
        'homeDescription': '',
        'schoolDistrict': '',
        'currentMonth': '',
        'total': '',
        'street': '',
        'zipcode': '',
        'city': '',
        'state': '',
        'latitude': '',
        'longitude': '',
        'homeDetails': '',
        'photoGallery': '',
        'homeInfo': '',
        'count': '',
        'image': '',
        'useCode': '',
        'bedrooms': '',
        'bathrooms': '',
        'finishedSqFt': '',
        'lotSizeSqFt': '',
        'yearBuilt': '',
        'yearUpdated': '',
        'numFloors': '',
        'numRooms': '',
        'roof': '',
        'parkingType': '',
        'heatingSystem': '',
        'coolingSystem': '',
        'appliances': '',
        'floorCovering': '',
        'architecture': '',
        'message': 'ok'
    }

    root = ET.XML(xml_str)
    code = root.find('message').findtext("code")
    if code != '0':
        result['message'] = root.find('message').findtext("text")
        return result

    response = root.find('response')
    if response is None:
        result['message'] = "response is None"
        return result

    pageViewCount = response.find('pageViewCount')
    address = response.find('address')
    links = response.find('links')
    images = response.find('images')
    editedFacts = response.find('editedFacts')

    result['zpid'] = response.findtext("zpid")
    result['homeDescription'] = response.findtext("homeDescription")
    result['schoolDistrict'] = response.findtext("schoolDistrict")

    # pageViewCount
    if pageViewCount is not None:
        result['currentMonth'] = pageViewCount.findtext("currentMonth")
        result['total'] = pageViewCount.findtext("total")

    # address
    if address is not None:
        result['street'] = address.findtext("street")
        result['zipcode'] = address.findtext("zipcode")
        result['city'] = address.findtext("city")
        result['state'] = address.findtext("state")
        result['latitude'] = address.findtext("latitude")
        result['longitude'] = address.findtext("longitude")

    # links
    if links is not None:
        result['homeDetails'] = links.findtext("homeDetails")
        result['photoGallery'] = links.findtext("photoGallery")
        result['homeInfo'] = links.findtext("homeInfo")

    # images
    if images is not None:
        result['count'] = images.findtext("count")
        result['image'] = images.find("image").findtext("url")

    # editedFacts
    if editedFacts is not None:
        result['useCode'] = editedFacts.findtext("useCode")
        result['bedrooms'] = editedFacts.findtext("bedrooms")
        result['bathrooms'] = editedFacts.findtext("bathrooms")
        result['finishedSqFt'] = editedFacts.findtext("finishedSqFt")
        result['lotSizeSqFt'] = editedFacts.findtext("lotSizeSqFt")
        result['yearBuilt'] = editedFacts.findtext("yearBuilt")
        result['yearUpdated'] = editedFacts.findtext("yearUpdated")
        result['numFloors'] = editedFacts.findtext("numFloors")
        result['numRooms'] = editedFacts.findtext("numRooms")
        result['roof'] = editedFacts.findtext("roof")
        result['parkingType'] = editedFacts.findtext("parkingType")
        result['heatingSystem'] = editedFacts.findtext("heatingSystem")
        result['coolingSystem'] = editedFacts.findtext("coolingSystem")
        result['appliances'] = editedFacts.findtext("appliances")
        result['floorCovering'] = editedFacts.findtext("floorCovering")
        result['architecture'] = editedFacts.findtext("architecture")

    return result


# 数据写入表格
def write_file(filename, response_data):
    w = Workbook()
    ws = w.add_sheet("sheet1")

    # 写入表头
    i = 0
    for key in response_data[0].keys():
        ws.write(0, i, key)
        i = i + 1

    row = 1
    for data in response_data:
        j = 0
        try:
            for (k, v) in data.items():
                if v is None:
                    v = ''
                ws.write(row, j, str(v))
                j = j + 1
        except Exception, e:
            print e
        row = row + 1
    w.save(filename)


zws_id = "X1-ZWz18v2b6f97gr_75222"
response_data = []

for zpid in open("zpids.txt"):
    zpid = zpid.replace("\n", "")
    if len(zpid) == 0:
        print "zpid为空"
        continue
    try:
        print "正在获取详细数据。zpid = " + zpid
        url = "http://www.zillow.com/webservice/GetUpdatedPropertyDetails.htm?zws-id=%s&zpid=%s" % (zws_id, zpid)
        xml_data = get_data_by_zpid(url)
        if xml_data == '':
            print "通过zpid无法获取数据"
            continue

        dict_data = xml_2_dict(xml_data)
        if dict_data['message'] != "ok":
            print "获取数据异常。message = " + dict_data['message']
            continue

        response_data.append(dict_data)
        print "获取获取详细数据完成"
    except Exception, e:
        print e

print "数据获取完成，正在写入数据..."
filename = "zillow_" + str(int(time.time())) + ".xls"
write_file(filename, response_data)
print "数据写入完成，文件名:" + filename
