import socket
import time


def blocking_socket():
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    sock.send(b'GET / HTTP/1.0\r\n\r\n')
    response = b''
    chunk = sock.recv(1024)
    while chunk:
        response += chunk
        chunk = sock.recv(1024)
    return response


def multi_blocking_socket():
    for _ in range(10):
        blocking_socket()


if __name__ == '__main__':
    start = time.time()
    # print(blocking_socket())
    multi_blocking_socket()
    print(time.time() - start)
