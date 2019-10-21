import socket
import time


# OS
def no_blocking_socket():
    sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass

    while True:
        try:
            sock.send(b'GET / HTTP/1.0\r\n\r\n')
            break
        except OSError:
            pass

    response = b''

    while True:
        try:
            chunk = sock.recv(1024)
            while chunk:
                response += chunk
                chunk = sock.recv(1024)
            break
        except OSError:
            continue
    return response


def multi_no_blocking_socket():
    for _ in range(10):
        no_blocking_socket()


if __name__ == '__main__':
    start = time.time()
    # print(no_blocking_socket())
    multi_no_blocking_socket()
    print(time.time() - start)
