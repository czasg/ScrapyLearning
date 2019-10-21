__file__ = '博客'

"""
原文章来源于: https://mp.weixin.qq.com/s?__biz=MzIxMjY5NTE0MA==&mid=2247483720&idx=1&sn=f016c06ddd17765fd50b705fed64429c
原项目GitHub: https://github.com/denglj/aiotutorial

原生asyncio异步协程的使用。具体使用推荐官方文档 https://docs.python.org/zh-cn/3/library/asyncio-task.html
loop获取事件循环，asyncio.create_task则注册协程为"任务"，进入异步事件循环


import asyncio
import aiohttp
import time

loop = asyncio.get_event_loop()


async def fetch():
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get('http://www.baidu.com') as response:
            print(await response.read())


async def multi_fetch():
    await asyncio.gather(*[asyncio.create_task(fetch()) for _ in range(10)])


if __name__ == '__main__':
    start = time.time()
    loop.run_until_complete(fetch())  # 执行一次
    # loop.run_until_complete(multi_fetch())  # 执行十次
    print(time.time() - start)
"""

"""
阻塞版本，基于socket编写，通过与目标服务器建立连接后，发送HTTP协议获取请求数据


import socket
import time


def blocking_socket(response=b''):
    sock = socket.socket()
    sock.connect(('www.baidu.com', 80))
    sock.send(b'GET / HTTP/1.0\r\n\r\n')
    chunk = sock.recv(1024)
    while chunk:
        response += chunk
        chunk = sock.recv(1024)
    return response


def mutil_blocking_socket():
    return [blocking_socket() for _ in range(10)].__len__()


if __name__ == '__main__':
    start = time.time()
    # blocking_socket()  # 执行一次
    # mutil_blocking_socket()  # 执行十次
    print(time.time() - start)
"""

"""
非阻塞式socket，但是实际效果与阻塞是相同的，因为及时处于非阻塞状态，但CPU并没有合理的使用非阻塞状态的时间
而是不同的轮询连接是否已经建立并不断的试错直至发送或读写成功


import socket
import time


def no_blocking_socket(response=b''):
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
            continue

    while True:
        try:
            chunk = sock.recv(1024)
            while chunk:
                response += chunk
                chunk = sock.recv(1024)
            return response
        except OSError:
            pass


def multi_no_blocking_socket():
    return [no_blocking_socket() for _ in range(10)].__len__()


if __name__ == '__main__':
    start = time.time()
    # no_blocking_socket()  # 执行一次
    # multi_no_blocking_socket()  # 执行十次
    print(time.time() - start)
"""

"""
解决上述问题的最好办法，就是由操作系统代替我们去轮询事件的发生。
OS已经将I/O封装为读写两种事件，故我们可以在此基础上进行对应的回调开发


import socket
import time

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stop_loop = 10


class Crawler:
    def __init__(self, flag=10):
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
        selector.register(self.sock.fileno(), EVENT_WRITE, self.on_send)  # fileno()获取当前socket套接字的文件描述符，并绑定事件回调

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
            stop_loop -= self.flag
            selector.unregister(self.sock.fileno())


def loop():  # 事件循环，由操作系统通知那个事件发生了，应该对应执行那些事件的回调。
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


if __name__ == '__main__':
    start = time.time()
    Crawler(10).fetch()  # 执行一次
    # [Crawler(1).fetch() for _ in range(10)]  # 执行十次
    loop()
    print(time.time() - start)
"""

"""
我们以协程的形式来编写代码，定义Future对象和Task对象
流程为：
1、创建Crawler对象，调用fetch函数得到一个协程
2、将此协程装于Task用来创建任务实例，在任务中会主动触发协程的send函数来启动协程
3、此时协程已触发，并注册事件 selector.register(self.sock.fileno(), EVENT_WRITE, _on_send)
4、loop事件轮询，当套接字的文件描述符状态变为可写状态时，触发回调方法_on_send
5、_on_send方法执行Future中的set_result方法，此时在此方法中会调用一次future注册的回调函数，继续触发任务Task中协程的send方法，回到协程上次暂停的状态
6、注销事件EVENT_WRITE。发送HTTP协议请求。再注册事件 selector.register(self.sock.fileno(), EVENT_READ, _on_recv)
7、loop事件轮询，当套接字的文件描述符变为可读状态时，触发回调方法_on_recv
8、_on_recv方法执行Future中的set_result方法，此时在方法中会初始化result为sock.recv(1024)的值，并执行注册的回调函数，将此结果继续传递至协程上回暂停的地方
9、由于一直没有注销事件EVENT_READ，故会一直驱动事件轮询直至结束
10、Task、Future、Crawler、loop这四个就这么神奇的串联在一起了，不可思议的说。


import socket
import time

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stop_loop = 10


class Future:
    # 用于存放未来可能出现的数据，当出现时执行一次回调函数
    # 此种的result仅作为一个中转，实际还是通过回调返回给协程

    def __init__(self):
        self.result = None
        self.callback = None

    def set_callback(self, func):
        self.callback = func

    def set_result(self, result):
        self.result = result
        self.callback(self) if self.callback else None


class Task:
    # 用于启动协程，该类实例初始化时传入为协程对象，执行self.process方法
    # 调用协程的send方法，启动协程，并最后绑定回调函数

    def __init__(self, co_routine):
        self.co_routine = co_routine
        future = Future()
        self.process(future)

    def process(self, future):
        try:
            next_future = self.co_routine.send(future.result)
        except StopIteration:
            return
        next_future.set_callback(self.process)


class Crawler:
    def __init__(self, flag=10):
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

        def _on_recv():
            future.set_result(self.sock.recv(1024))

        selector.register(self.sock.fileno(), EVENT_WRITE, _on_send)
        yield future
        selector.unregister(self.sock.fileno())
        self.sock.send(b'GET / HTTP/1.0\r\n\r\n')
        selector.register(self.sock.fileno(), EVENT_READ, _on_recv)
        while True:
            chunk = yield future  # 在此处轮询EVENT_READ事件，直至所有数据加载完毕
            if chunk:
                self.response += chunk
            else:
                global stop_loop
                stop_loop -= self.flag
                return self.response


def loop():
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


if __name__ == '__main__':
    start = time.time()
    Task(Crawler(10).fetch())  # 传入协程fetch，使用Task实例化调用协程的send方法来启动协程
    # [Task(Crawler(1).fetch()) for _ in range(10)]  # 同理，启动十个协程任务
    loop()
    print(time.time() - start)
"""

"""
拆离上述代码块，分离出fetch和read



import socket
import time

from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
stop_loop = 10


def fetch(sock):
    sock.setblocking(False)
    try:
        sock.connect(('www.baidu.com', 80))
    except BlockingIOError:
        pass

    future = Future()

    def _on_send():
        future.set_result(None)

    selector.register(sock.fileno(), EVENT_WRITE, _on_send)
    yield from future
    selector.unregister(sock.fileno())
    return future


def read(sock, future, flag, response=b''):
    def _on_recv():
        future.set_result(sock.recv(1024))

    selector.register(sock.fileno(), EVENT_READ, _on_recv)
    chunk = yield from future
    while chunk:
        response += chunk
        chunk = yield from future
    selector.unregister(sock.fileno())
    global stop_loop
    stop_loop -= flag
    return response


def loop():
    while stop_loop:
        events = selector.select()
        for sock, mask in events:
            sock.data()


class Future:
    def __init__(self):
        self.result = None
        self.callback = None

    def set_callback(self, func):
        self.callback = func

    def set_result(self, result):
        self.result = result
        self.callback(self) if self.callback else None

    def __iter__(self):
        yield self
        return self.result


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
        next_future.set_callback(self.process)


class Crawler:
    def __init__(self, flag):
        self.flag = flag

    def fetch(self):
        sock = socket.socket()
        future = yield from fetch(sock)
        sock.send(b'GET / HTTP/1.0\r\n\r\n')
        response = yield from read(sock, future, self.flag)
        print(response)


if __name__ == '__main__':
    start = time.time()
    Task(Crawler(10).fetch())
    # [Task(Crawler(1).fetch()) for _ in range(10)]
    loop()
    print(time.time() - start)
"""
