import socketserver

from socket import socket, getdefaulttimeout


class Socket(socket):
    """
    这玩意是为了重写取出slots，以便拿到后序的的__path__属性
    """
    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        super(Socket, self).__init__(family, type, proto, fileno)

    def accept(self):
        fd, addr = self._accept()
        sock = Socket(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr


class MyServerThreadingMixIn(socketserver.ThreadingMixIn):
    """连接开启新线程"""
    """process_request函数是入口，开启一个线程进行后序的处理
    就是开启一个新的线程然后使用Handler去处理相关的数据
    """


class MyServerTCPServer(socketserver.TCPServer):

    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True):
        socketserver.BaseServer.__init__(self, server_address, RequestHandlerClass)
        self.socket = Socket(self.address_family, self.socket_type)
        if bind_and_activate:
            try:
                self.server_bind()
                self.server_activate()
            except:
                self.server_close()
                raise


class SocketHandler:
    """这玩意就应该自己重写一个
    用来管控从进入的所有socket

    这里放置中间件，不对，中间件需要初始化的过程添加进去。，所以在前面应该还有一个初始化的过程，把配置参数，中间件，处理间都加载机那里。
    配置参数的获取方式感觉可以参考Scrpay的setting构造，那玩意我还是没看懂，明天快乐呀，可以看看这玩意
    """
    def __init__(self):
        pass