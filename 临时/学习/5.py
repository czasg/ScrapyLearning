import socket
import time

from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
stop_loop = 10


class Future:
    def __init__(self):
        self.result = None
        self.callback = None

    def add_callback(self, func):
        self.callback = func

    def set_result(self, result):
        self.result = result
        if self.callback:
            self.callback(self)


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

        future = Future()

        def _on_send():
            future.set_result(None)

        selector.register(self.sock.fileno(), EVENT_WRITE, _on_send)
        yield future

        selector.unregister(self.sock.fileno())
        self.sock.send(b'GRT / HTTP/1.0\r\n\r\n')
        future = Future()

        def _on_recv():
            future.set_result(self.sock.recv(1024))

        selector.register(self.sock.fileno(), EVENT_READ, _on_recv)

        while True:
            chunk = yield future
            if chunk:
                self.response += chunk
            else:
                selector.unregister(self.sock.fileno())
                global stop_loop
                stop_loop -= self.flag
                print(self.response)


class Task:
    def __init__(self, co_routine):
        self.co_routine = co_routine
        future = Future()
        self.process(future)

    def process(self, future):
        try:
            next_future = self.co_routine.send(future.result)
        except StopIteration:
            return
        next_future.add_callback(self.process)


def co_routine():
    Task(Crawler(10).fetch())


def multi_ro_routine():
    for _ in range(10):
        Task(Crawler(1).fetch())


def loop():  # 事件轮询
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


if __name__ == '__main__':
    start = time.time()
    # co_routine()
    multi_ro_routine()
    loop()
    print(time.time() - start)
