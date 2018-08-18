# _*_coding:utf-8_*_

import json
from threading import Thread

import admin
import config
import news
import web

urls = (
    '/spider', 'Spider',
    '/news', 'News',
    '/users', 'Users',
    '/news/delete/(.*)', 'DeleteNews',
    '/login', 'Login',
    '/', 'Index'
)
app = web.application(urls, globals())


class Spider:
    def GET(self):
        flag = web.input()["flag"]
        if flag == "3":
            config.isStop = True
        else:
            config.isStop = False
            t = Thread(target=news.spider, args=(flag,))
            t.start()

        web.header("Access-Control-Allow-Origin", "*")
        return []


class News:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        return news.get_list()


class Users:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        return admin.get_list()


class DeleteNews:
    def GET(self, newsId):
        web.header("Access-Control-Allow-Origin", "*")
        news.deleteOne(newsId)
        return []


class Index:
    def GET(self):
        web.header("Access-Control-Allow-Origin", "*")
        return open(r'static/index.html', 'r').read()


class Login:
    def POST(self):
        userInput = web.data().decode("utf-8")
        userJson = json.loads(userInput)
        account = userJson["account"]
        password = userJson["password"]
        user = admin.findOne(account)

        res = {"state": "true", "account": account}

        web.header("Access-Control-Allow-Origin", "*")
        if user is None:
            res["state"] = "false"
            res["msg"] = "用户不存在"
            return res

        if password == user["password"]:
            res["role"] = user["role"]
            return res
        else:
            res["state"] = "false"
            res["msg"] = "用户密码错误"
            return res


if __name__ == "__main__":
    app.run()
