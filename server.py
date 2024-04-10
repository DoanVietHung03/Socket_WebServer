import pathlib
import socket
from os import error
import threading

HOST = "127.0.0.1"
PORT = 8080

SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    SERVER.bind((HOST,PORT))
    print(f'* Running on http://{HOST}:{PORT}')
except socket.error as e:
    print(f'socket error: {e}')


def _start():
    SERVER.listen()
    while True:
        conn, addr = SERVER.accept()
        thread = threading.Thread(target=_handle, args=(conn, addr))
        thread.start()

def _handle(conn, addr):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        request_line = data.split('\r\n')[0]
        request_method = request_line.split(' ')[0]
        request_url = (request_line.split(' ')[1]).strip('/')
        p = pathlib.Path('index.html')
        if request_method == 'GET':
            if p.exists() == False:
                #404 page
                url = '404.html'
                Content_type = 'text/html'
                data = _read_file(url, Content_type)
                conn.send(data)
                print(data.decode())
                conn.close()
                break
            if request_url == '':
                #index page
                url = 'index.html'
                Content_type = 'text/html'
            else: 
                url = request_url
                Content_type = 'text/html'
            data = _read_file(url, Content_type)
            conn.send(data)
            print(data.decode())
            conn.close()
            break
        elif request_method == 'POST':
            print(data)
            if 'Username=admin' in data and data.rsplit('&',1)[1] == 'Password=123456':
                if request_url == '':
                    #images page
                    url = 'infor.html'
                    Content_type = 'text/html'
                else: 
                    url = request_url
                    Content_type = 'text/html'
            else:
                if request_url == '':
                    #401 page
                    url = '401.html'
                    Content_type = 'text/html'
                else: 
                    url = request_url
                    Content_type = 'text/html'
            data = _read_file(url, Content_type)
            conn.send(data)
            print(data.decode())
            conn.close()
            break

def _read_file(Name_file,Content_type):
    f = open(Name_file, 'rb')
    if Name_file == '401.html':
        fdata = _response_401(Content_type)
    else:
        fdata = _response_header(Content_type)
    fdata += f.read()
    return fdata

def _response_header(Content_type):
    message_header = 'HTTP/1.1 200 OK\r\n'
    message_header += 'Connection: Close\r\n'
    message_header += f'Content-type: {Content_type}\r\n'
    message_header += '\r\n'
    message_header = message_header.encode()
    return message_header

def _response_404(Content_type):
    message = 'HTTP/1.1 404 Not Found\r\n'
    message += 'Connection: Close\r\n'
    message += f'Content-type: {Content_type}\r\n'
    message += '\r\n'
    message = message.encode()
    return message

def _response_401(Content_type):
    message_header = 'HTTP/1.1 401 Unauthorized\r\n'
    message_header += 'Connection: Close\r\n'
    message_header += f'Content-type: {Content_type}; charset=UTF-8\r\n'
    message_header += '\r\n'
    message_header = message_header.encode()
    return message_header

if __name__ == '__main__':
    _start()
