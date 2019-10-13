TARGET_URL = 'https://g.alicdn.com/secdev/sufei_data/3.7.2/index.js'
INJECT_TEXT = 'Object.defineProperties(navigator,{webdriver:{get:() => undefined}});'

t0 ='Object.defineProperties(navigator,{webdriver:{get:() => false}});'
t1 = 'window.navigator.chrome = {runtime: {},// etc.};'
t2 = '''
Object.defineProperty(navigator, 'languages', {
      get: () => ['en-US', 'en']
    });
'''
t3 = '''
Object.defineProperty(navigator, 'plugins', {
    get: () => [1, 2, 3, 4, 5,6],
  });
'''
t4 = '''
           Object.defineProperties(navigator,{
             userAgent:{
               get: () => Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36;
             }
           })
'''


def response(flow):
    if flow.request.url.startswith(TARGET_URL):
        flow.response.text = INJECT_TEXT + flow.response.text
        print('注入成功')

    if 'um.js' in flow.request.url or '114.js' in flow.request.url:
        # 屏蔽selenium检测
        flow.response.text = flow.response.text + 'Object.defineProperties(navigator,{webdriver:{get:() => false}}); '
