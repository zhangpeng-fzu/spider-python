from django.http import HttpResponse
import json
from ..service import user_service
from ..service import whiteip_service
import collections


def login(request):
    if request.method == 'POST':
        post_body = str(request.body, encoding="utf8")
        user_json = json.loads(post_body)
        account = user_json["account"]
        password = user_json["password"]
        user_arr = user_service.find_one(account)
        res = {"state": "true", "account": account}

        user_ip = request.META['REMOTE_ADDR']
        if not whiteip_service.check_ip(user_ip):
            res["state"] = "false"
            res["msg"] = "用户IP不在白名单中"
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")

        if len(user_arr) == 0:
            res["state"] = "false"
            res["msg"] = "用户不存在"
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")

        user = user_arr[0]
        if password != user.PASSWORD:
            res["state"] = "false"
            res["msg"] = "用户密码错误"
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")

        res["role"] = user.ROLE
        response = HttpResponse(json.dumps(res, ensure_ascii=False), status=200,
                                content_type="application/json,charset=utf-8", )
        response["Access-Control-Allow-Origin"] = "*"
        return response


def user_list(request):
    users = user_service.get_list()
    objects_list = []
    for User in users:
        d = collections.OrderedDict()
        d['id'] = User.id
        d['account'] = User.ACCOUNT
        d['role'] = User.ROLE
        d['createTime'] = str(User.CREATE_TIME)
        objects_list.append(d)
    res = {"data": objects_list}

    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")


def delete(request):
    ids = request.GET["ids"]
    user_service.delete(ids)
    return HttpResponse(json.dumps({}, ensure_ascii=False), content_type="application/json,charset=utf-8")
