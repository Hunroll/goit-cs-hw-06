import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

import json
import socket

class HttpHandler(BaseHTTPRequestHandler):
    socket_server = None

    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        
    def do_POST(self):
        data = self.rfile.read(int(self.headers['Content-Length']))
        print(data)
        data_parse = urllib.parse.unquote_plus(data.decode())
        print(data_parse)
        data_dict = json.dumps({key: value for key, value in [el.split('=') for el in data_parse.split('&')]})
        print(data_dict)
        self.socket_send(data_dict)
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('www/index.html')
        elif pr_url.path == '/message.html' or pr_url.path == '/message':
            self.send_html_file('www/message.html')
        elif pr_url.path == '/style.css':
            self.send_html_file('www/style.css')
        elif pr_url.path == '/logo.png':
            self.send_html_file('www/logo.png')
        else:
            self.send_html_file('www/error404.html', 404)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())

    def send_static(self):
        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())
            
    def socket_send(self, data: dict):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(HttpHandler.socket_server)
            print(f'Connection established {HttpHandler.socket_server}')
            print(f'Send data: {data}')
            sock.send(str(data).encode())
        print(f'Data transfer completed')



def run(socket_host, socket_port, server_class=HTTPServer, handler_class=HttpHandler):
    HttpHandler.socket_server = (socket_host, socket_port)
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        print("Interrupted")
        http.server_close()


if __name__ == '__main__':
    run()