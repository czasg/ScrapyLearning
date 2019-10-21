import socket
import time

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stop_loop = 10


class Crawler:
    def __init__(self, flag):
        self.flag = flag
        self.sock = None
        self.response = b''

    def fetch(self):
        self.sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(('www.baidu.com', 80))
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, self.on_send)

    def on_send(self):
        selector.unregister(self.sock.fileno())
        self.sock.send(b'GET / HTTP/1.0\r\n\r\n')
        selector.register(self.sock.fileno(), EVENT_READ, self.on_recv)

    def on_recv(self):
        chunk = self.sock.recv(1024)
        if chunk:
            self.response += chunk
        else:
            global stop_loop
            selector.unregister(self.sock.fileno())
            stop_loop -= self.flag
            print(self.response)


def loop():
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


def fetch():
    Crawler(10).fetch()


def multi_fetch():
    for _ in range(10):
        Crawler(1).connect()


if __name__ == '__main__':
    start = time.time()
    # fetch()
    multi_fetch()
    loop()
    print(time.time() - start)
