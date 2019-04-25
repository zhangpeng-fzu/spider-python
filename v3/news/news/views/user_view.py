from django.http import HttpResponse
import json
from ..service import user_service


def login(request):
    if request.method == 'POST':
        postBody = str(request.body, encoding="utf8")
        userJson = json.loads(postBody)
        account = userJson["account"]
        password = userJson["password"]
        # user = user_service.findOne(account)

        res = {"state": "true", "account": account}

        # if user is None:
        #     res["state"] = "false"
        #     res["msg"] = "用户不存在"
        #     return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")
        #
        # if password != user["password"]:
        #     res["state"] = "false"
        #     res["msg"] = "用户密码错误"
        #     return HttpResponse(json.dumps(res, ensure_ascii=False), content_type="application/json,charset=utf-8")

        # res["role"] = user["role"]
        response = HttpResponse(json.dumps(res, ensure_ascii=False),status=200, content_type="application/json,charset=utf-8",)
        response["Access-Control-Allow-Origin"] = "*"
        return response
