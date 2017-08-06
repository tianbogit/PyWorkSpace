# coding:utf-8

import time

HTML_ROOT_DIR = "./static"

class Application(object):
    '''自定义通用的web框架'''

    # 初始化路由信息
    def __init__(self,urls):
        self.urls = urls

    # 匹配路由
    def __call__(self, env, start_response):
        path = env.get("PATH_INFO", "/")
        # /static/index.html
        if path.startswith("/static"):
            file_name = path[7:]
            # 打开文件，读取内容
            try:
                file = open(HTML_ROOT_DIR + file_name, "rb")
            except IOError:
                # 代表未找到路由信息，404错误
                status = "404 Not Found"
                headers = []
                start_response(status, headers)
                return "not found"
            else:
                file_data = file.read()
                file.close()

                status = "200 OK"
                headers = []
                start_response(status, headers)
                return file_data.decode("utf-8")


        for url,handler in self.urls:
            if path == url:
                return handler(env,start_response)
        # 未匹配到
        status = '404 Not Found'
        headers = []
        start_response(status,headers)
        return 'not found'

def showtime(env,start_response):
    status = '200 OK'
    headers = [
        ('Content-Type', 'text/plain')
    ]
    start_response(status, headers)
    return str(time.time())

def sayhello(env,start_response):
    status = '200 OK'
    headers = [
        ('Content-Type','text/plain')
    ]
    start_response(status,headers)
    return 'say hello'

def helloworld(env,start_response):
    status = '200 OK'
    headers =[
        ('Content-Type','text/plain')
    ]
    start_response(status,headers)
    return 'hello world'


urls = [
    ('/', showtime),
    ('/sayhello',sayhello),
    ('/helloworld',helloworld)
]
app = Application(urls)
# if __name__ == '__main__':
#     urls = [
#         ('/', showtime),
#         ('/sayhello',sayhello),
#         ('/helloworld',helloworld)
#     ]
#     app = Application(urls)
#
#     webServer = WebServer(app)
#     webServer.bind(8000)
#     webServer.start()