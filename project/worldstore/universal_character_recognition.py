import os
from datetime import datetime
from wsgiref.handlers import format_date_time
from time import mktime
import hashlib
import base64
import hmac
from urllib.parse import urlencode
import json
import requests
from PIL import Image

'''
1、通用文字识别,图像数据base64编码后大小不得超过10M
2、appid、apiSecret、apiKey请到讯飞开放平台控制台获取并填写到此demo中
3、支持中英文,支持手写和印刷文字。
4、在倾斜文字上效果有提升，同时支持部分生僻字的识别
'''

APPId = "xxx"  # 控制台获取
APISecret = "xxx"  # 控制台获取
APIKey = "xxx"  # 控制台获取


class AssembleHeaderException(Exception):
    def __init__(self, msg):
        self.message = msg


class Url:
    def __init__(self, host, path, schema):
        self.host = host
        self.path = path
        self.schema = schema
        pass


# calculate sha256 and encode to base64
def sha256base64(data):
    sha256 = hashlib.sha256()
    sha256.update(data)
    digest = base64.b64encode(sha256.digest()).decode(encoding='utf-8')
    return digest


def parse_url(requset_url):
    stidx = requset_url.index("://")
    host = requset_url[stidx + 3:]
    schema = requset_url[:stidx + 3]
    edidx = host.index("/")
    if edidx <= 0:
        raise AssembleHeaderException("invalid request url:" + requset_url)
    path = host[edidx:]
    host = host[:edidx]
    u = Url(host, path, schema)
    return u


# build websocket auth request url
def assemble_ws_auth_url(requset_url, method="POST", api_key="", api_secret=""):
    u = parse_url(requset_url)
    host = u.host
    path = u.path
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    signature_origin = "host: {}\ndate: {}\n{} {} HTTP/1.1".format(host, date, method, path)
    signature_sha = hmac.new(api_secret.encode('utf-8'), signature_origin.encode('utf-8'),
                             digestmod=hashlib.sha256).digest()
    signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')
    authorization_origin = "api_key=\"%s\", algorithm=\"%s\", headers=\"%s\", signature=\"%s\"" % (
        api_key, "hmac-sha256", "host date request-line", signature_sha)
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    values = {
        "host": host,
        "date": date,
        "authorization": authorization
    }

    return requset_url + "?" + urlencode(values)


url = 'https://api.xf-yun.com/v1/private/sf8e6aca1'


def request(name, base64_f):
    out_name = convert_image(name, base64_f)
    with open(out_name, "rb") as f:
        image_bytes = f.read()
    body = {
        "header": {
            "app_id": APPId,
            "status": 3
        },
        "parameter": {
            "sf8e6aca1": {
                "category": "ch_en_public_cloud",
                "result": {
                    "encoding": "utf8",
                    "compress": "raw",
                    "format": "json"
                }
            }
        },
        "payload": {
            "sf8e6aca1_data_1": {
                "encoding": "jpg",
                "image": str(base64.b64encode(image_bytes), 'UTF-8'),
                "status": 3
            }
        }
    }

    request_url = assemble_ws_auth_url(url, "POST", APIKey, APISecret)

    headers = {'content-type': "application/json", 'host': 'api.xf-yun.com', 'app_id': APPId}
    response = requests.post(request_url, data=json.dumps(body), headers=headers)

    tempResult = json.loads(response.content.decode())

    finalResult = base64.b64decode(tempResult['payload']['result']['text']).decode()
    finalResult = finalResult.replace(" ", "").replace("\n", "").replace("\t", "").strip()
    word = json.loads(finalResult)["pages"][0]["lines"][0]["words"][0]["content"]
    os.remove(out_name)
    return word


def convert_image(name, f1_base64):
    img_data = base64.b64decode(f1_base64)
    filename = name + '.png'
    file = open(filename, 'wb')
    file.write(img_data)
    file.close()

    im = Image.open(filename)
    x, y = im.size
    try:
        # 填充白色背景
        p = Image.new('RGBA', im.size, (255, 255, 255))
        p.paste(im, (0, 0, x, y), im)
        p.save(name + '-out.png')
        os.remove(filename)
        return name + '-out.png'
    except Exception as exc:
        print(exc)


if __name__ == '__main__':
    f_base64 = "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"
    request(str(11), f_base64)
