from django.http import HttpResponse
import json
from ..service import user_service
import collections

def login(request):
    if request.method == 'POST':
        postBody = str(request.body, encoding="utf8")
        userJson = json.loads(postBody)
        account = userJson["account"]
        password = userJson["password"]
        userList = user_service.findOne(account)

        res = {"state": "true", "account": account}

        if len(userList) == 0:
            res["state"] = "false"
            res["msg"] = "用户不存在"
            return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")

        user = userList[0]
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
        d['account'] = User.ACCOUNT
        d['role'] = User.ROLE
        d['createTime'] = str(User.CREATE_TIME)
        objects_list.append(d)
    res = {"data": objects_list}

    return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")
