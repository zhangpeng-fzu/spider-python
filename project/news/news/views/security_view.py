from django.http import HttpResponse
import json
from ..service import whiteip_service
import collections


def whiteip(request):
    if request.method == 'POST':
        post_body = str(request.body, encoding="utf8")
        json_obj = json.loads(post_body)
        ip = json_obj["ip"]
        name = json_obj["name"]
        whiteip_service.save(ip, name)
        return HttpResponse(json.dumps({}, ensure_ascii=False), content_type="application/json,charset=utf-8")
    else:
        whiteips = whiteip_service.get_list()
        objects_list = []
        for WhiteIp in whiteips:
            d = collections.OrderedDict()
            d['id'] = WhiteIp.id
            d['ip'] = WhiteIp.IP
            d['name'] = WhiteIp.NAME
            objects_list.append(d)
        res = {"data": objects_list}
        return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def deleteAll(request):
    ids = request.GET["ids"]
    whiteip_service.delete(ids)
    return HttpResponse(json.dumps({}, ensure_ascii=False), content_type="application/json,charset=utf-8")
