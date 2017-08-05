# coding:utf-8

import socket
import re

from multiprocessing import Process

HTML_ROOT_DIR = './static'


class WebServer(object):
    '''
    简单的webserver
    '''

    def __init__(self):
        self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.sock_server.listen(128)
        while True:
            sock_client, addr = self.sock_server.accept()
            print('[%s,%s]用户已连接......' % addr)
            handle_client_process = Process(target=self.handle_client, args=(sock_client,))
            handle_client_process.start()
            sock_client.close()

    def handle_client(self, sock_client):
        '''处理客户端请求'''
        recv_data = sock_client.recv(1024)
        #print('请求数据：', recv_data)
        req_lines = recv_data.splitlines()
        #for line in req_lines:
        #    print(line)

        req_start_line = req_lines[0]
        #print(req_start_line.decode('utf-8'))
        file_name = re.match(r'\w+ +(/[^ ]*) ', req_start_line.decode('utf-8')).group(1)
        if '/' == file_name:
            file_name = "/index.html"

        try:
            file = open(HTML_ROOT_DIR + file_name, 'rb')
        except IOError:
            resp_start_line = 'HTTP/1.1 404 Not Found\r\n'
            resp_headers = 'Server: My Web Server\r\n'
            resp_body = 'The file is not found!'
        else:
            file_data = file.read()
            file.close()

            resp_start_line = 'HTTP/1.1 200 OK\r\n'
            resp_headers = 'Server: My Web Server\r\n'
            resp_body = file_data.decode('utf-8')

        # 构造响应内容
        resp_data = resp_start_line + resp_headers + '\r\n' + resp_body
        #print('构造响应内容：', resp_data)

        # response
        sock_client.send(bytes(resp_data, 'utf-8'))

        # 关闭客户端连接
        sock_client.close()

    def bind(self, port):
        self.sock_server.bind(('', port))


def main():
    webServer = WebServer()
    webServer.bind(8000)
    webServer.start()


if __name__ == '__main__':
    main()