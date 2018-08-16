import web

urls = (
    '/index', 'index',
    '/blog/\d+', 'blog',
    '/(.*)', 'hello'
)
app = web.application(urls, globals())


class hello:
    def GET(self, name):
        return 'hello ' + name


class index:
    def GET(self):
        return 'index method'


class blog:
    def GET(self):
        return 'blog GET method'

    def POST(self):
        return 'blog POST method'


if __name__ == "__main__":
    app.run()
