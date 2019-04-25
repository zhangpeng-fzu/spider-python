from django.http import HttpResponse
import json
from threading import Thread
from ..service import user_service
from ..service import spider_service
from ..config import constants


def list(request):
    return


def delete(request):
    return


def spider(request):
    flag = request.GET["flag"]
    source = request.GET["source"]
    if flag == "3":
        constants.isStop = True
        print("已成功停止获取数据")
    else:
        constants.isStop = False
        t = Thread(target=spider_service.spider, args=(flag,source))
        t.start()
    res = {"state": "true"}
    response = HttpResponse(json.dumps(res, ensure_ascii=False), status=200,
                            content_type="application/json,charset=utf-8", )
    response["Access-Control-Allow-Origin"] = "*"
    return response
