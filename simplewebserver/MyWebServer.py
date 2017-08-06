# coding:utf-8

import socket
import re
import sys

from multiprocessing import Process

HTML_ROOT_DIR = './static'
WSGI_PY = './wsgipy'

class WebServer(object):
    '''
    简单的webserver
    '''

    def __init__(self,application):
        '''application：框架'''
        self.sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.app = application

    def start(self):
        self.sock_server.listen(128)
        while True:
            sock_client, addr = self.sock_server.accept()
            print('[%s,%s]用户已连接......' % addr)
            handle_client_process = Process(target=self.handle_client, args=(sock_client,))
            handle_client_process.start()
            sock_client.close()

    def start_response(self, status, headers):
        """
                 status = "200 OK"
            headers = [
                ("Content-Type", "text/plain")
            ]
            star
                """
        resp_headers = 'HTTP/1.1 ' + status + '\r\n'
        for header in headers:
            resp_headers += '%s: %s\r\n' % header

        self.resp_headers = resp_headers

    def handle_client(self, sock_client):
        '''处理客户端请求'''
        recv_data = sock_client.recv(1024)
        #print('请求数据：', recv_data)
        req_lines = recv_data.splitlines()
        #for line in req_lines:
        #    print(line)

        req_start_line = req_lines[0]
        #print(req_start_line.decode('utf-8'))
        file_name = re.match(r"\w+ +(/[^ ]*) ", req_start_line.decode("utf-8")).group(1)
        method = re.match(r"(\w+) +/[^ ]* ", req_start_line.decode("utf-8")).group(1)

        env = {
            "PATH_INFO": file_name,
            "METHOD": method
        }
        response_body = self.app(env, self.start_response)

        response = self.resp_headers + "\r\n" + response_body

        # 向客户端返回响应数据
        sock_client.send(bytes(response, "utf-8"))

        # 关闭客户端连接
        sock_client.close()

    def bind(self, port):
        self.sock_server.bind(('', port))


def main():
    sys.path.insert(1,WSGI_PY)
    if len(sys.argv) < 2:
        sys.exit("python MyWebServer.py Module:app")
    module_name, app_name = sys.argv[1].split(':')
    m = __import__(module_name)
    app = getattr(m,app_name)
    webServer = WebServer(app)
    webServer.bind(8000)
    webServer.start()


if __name__ == '__main__':
    main()