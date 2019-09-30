import socketserver
import logging

from socket import socket, getdefaulttimeout

from pyws.protocol import WebSocketProtocol, ProtocolProperty
from pyws.route import Route
from pyws.middlewares import mwManager
from pyws.connector import Connector, ConnectManager

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ERROR_COUNT = 4


class Socket(socket):
    """
    这玩意是为了重写取出slots，以便拿到后序的的__path__属性
    """
    __slots__ = ["_io_refs", "_closed", "__route__"]

    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        super(Socket, self).__init__(family, type, proto, fileno)

    def accept(self):
        fd, addr = self._accept()
        sock = Socket(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr


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

    def verify_request(self, request, client_address):
        """验证是否为WebSocket升级连接"""
        try:
            path, key = WebSocketProtocol.parsing(request.recv(1024))
            if path in Route.routes:
                request.send(key)
                request.__route__ = path
                return True
        except:
            pass
        return False


class MyServerThreadingMixIn(socketserver.ThreadingMixIn):
    """连接开启新线程
    process_request函数是入口，开启一个线程进行后序的处理
    就是开启一个新的线程然后使用Handler去处理相关的数据
    """


class SocketHandler:
    """这玩意就应该自己重写一个
    用来管控从进入的所有socket

    这里放置中间件，不对，中间件需要初始化的过程添加进去。，所以在前面应该还有一个初始化的过程，把配置参数，中间件，处理间都加载机那里。
    配置参数的获取方式感觉可以参考Scrpay的setting构造，那玩意我还是没看懂，明天快乐呀，可以看看这玩意
    """

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        try:
            self.setup()
            self.handle()  # 在这里循环
        except:
            pass
        finally:
            self.finish()

    def setup(self):  # 这里走一次性中间件的处理
        self.conn = mwManager.daemon_process(self, self.request)  # 如果有验证，就创建一个验证的用户
        if not self.conn:
            self.conn = Connector(self.request, self.client_address)  # 没有验证，就自己随机一个字串作为唯一id，不是很推荐呀
        ConnectManager.add_connector(self.conn.name, self.conn.client_address, self.conn)
        logger.info('Connect From %s:%s' % self.client_address)

    def handle(self):
        error_count = 0
        func = Route.get(self.request.__route__)
        try:
            while error_count < ERROR_COUNT:
                info = mwManager.process(self.request, self.request.recv(1024), func)  # 中间件最后就返回一个这样的玩意嘛
                if info:
                    self.request.send(info)
                    continue
        except:
            pass

    def finish(self):
        logger.warning('%s:%s Connect Close' % self.client_address)
        try:
            ConnectManager.clear(self.conn.name, self.conn.client_address, self.conn.clear_level)
        except:
            pass


class Pyws(MyServerThreadingMixIn, MyServerTCPServer):
    """
    路径加载完了
    中间件也加载完了
    """

    def __init__(self,
                 routes_module,
                 address='127.0.0.1', port=8866,
                 RequestHandlerClass=SocketHandler,
                 request_queue_size=5,
                 middleware=None):
        logger.info('Server Start ...')
        logger.info('Server Address is %s:%d' % (address, port))
        server_address = (address, port)
        ProtocolProperty.set_location(server_address)
        self.add_routes(routes_module)
        self.add_middleware(middleware)
        self.request_queue_size = request_queue_size
        super(Pyws, self).__init__(server_address, RequestHandlerClass)

    def add_routes(self, module):
        Route.add_routes(module)

    def add_middleware(self, middleware):
        mwManager.auto_add(middleware)
