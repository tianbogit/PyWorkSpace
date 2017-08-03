# coding:utf-8

import socket

from multiprocessing import Process

def handle_client(sock_client):
    recv_data = sock_client.recv(1024)
    print('请求数据：',recv_data)

    # 构造响应内容
    resp_start_line = 'HTTP/1.1 200 OK\r\n'
    resp_headers = 'Server: My Web Server\r\n'

    resp_body = 'My First Web Server'
    resp_data = resp_start_line+resp_headers+'\r\n'+resp_body
    print('构造响应内容：',resp_data)

    # response
    sock_client.send(bytes(resp_data,'utf-8'))

    # 关闭客户端连接
    sock_client.close()


if __name__=='__main__':
    sock_server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sock_server.bind(('',8000))
    sock_server.listen(128)

    while True:
       sock_client,addr = sock_server.accept()
       print('[%s,%s]用户已连接......' % addr)      
       handle_client_process = Process(target=handle_client,args=(sock_client,))
       handle_client_process.start()
       sock_client.close()

    

