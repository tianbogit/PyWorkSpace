# coding:utf-8

def application(env,start_response):
    status = '200 OK'
    headers =[
        ('Content-Type','text/plain')
    ]
    start_response(status,headers)
    return "hello world"