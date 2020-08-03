from django.http import HttpResponse
import json
from threading import Thread
from ..service import news_service
from ..service import spider_service
from ..service import label_service
from ..config import constants
import collections


def news_list(request):
    news = news_service.get_list()
    objects_list = []
    for News in news:
        d = collections.OrderedDict()
        d['id'] = News.NEWS_ID
        d['title'] = News.TITLE
        d['source'] = News.SOURCE
        d['url'] = News.URL
        d['keywords'] = News.KEYWORDS
        d['createTime'] = str(News.CREATE_TIME)
        objects_list.append(d)
    res = {"data": objects_list}

    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def delete(request):
    news_id = request.GET["newsId"]
    news_service.delete(news_id)
    return HttpResponse(json.dumps({}, ensure_ascii=False), content_type="application/json,charset=utf-8")


def spider(request):
    flag = request.GET["flag"]
    source = request.GET["source"]
    if flag == "3":
        constants.isStop = True
        print("已成功停止获取数据")
    else:
        constants.isStop = False
        t = Thread(target=spider_service.spider, args=(flag, source))
        t.start()
    res = {"state": "true"}
    response = HttpResponse(json.dumps(res, ensure_ascii=False), status=200,
                            content_type="application/json,charset=utf-8", )
    response["Access-Control-Allow-Origin"] = "*"
    return response


def label(request):
    if request.method == 'POST':
        post_body = str(request.body, encoding="utf8")
        json_obj = json.loads(post_body)
        desc = json_obj["desc"]
        name = json_obj["name"]
        label_service.save(name, desc)
        return HttpResponse(json.dumps({}, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        whiteips = label_service.get_list()
        objects_list = []
        for WhiteIp in whiteips:
            d = collections.OrderedDict()
            d['id'] = WhiteIp.id
            d['name'] = WhiteIp.NAME
            objects_list.append(d)
        res = {"data": objects_list}
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def deleteLabel(request):
    ids = request.GET["ids"]
    label_service.delete(ids)
    return HttpResponse(json.dumps({}, ensure_ascii=False), content_type="application/json,charset=utf-8")
