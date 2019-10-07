import socketserver
import logging
import json

from socket import socket, getdefaulttimeout

from pyws.protocol import WebSocketProtocol, ProtocolProperty
from pyws.route import Route
from pyws.middlewares import mwManager
from pyws.connector import Connector, ConnectManager
from pyws.public import *

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class Socket(socket):
    __slots__ = ["_io_refs", "_closed", "__route__", "ws_sock"]

    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        super(Socket, self).__init__(family, type, proto, fileno)

    def accept(self):
        fd, addr = self._accept()
        sock = Socket(self.family, self.type, self.proto, fileno=fd)
        if getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        sock.ws_sock = sock  # 绑定目标
        return sock, addr

    def ws_recv(self, bufsize: int, flags: int = ...):
        return WebSocketProtocol.decode_msg(self.ws_sock.recv(bufsize))

    def ws_send(self, data, flags: int = ...):
        self.ws_sock.send(WebSocketProtocol
                          .encode_msg(json.dumps(data, ensure_ascii=False)
                                      .encode('utf-8')))


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

    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.func = Route.get(self.request.__route__)
        try:
            self.setup()
            self.handle()
        except:
            pass
        finally:
            self.finish()

    def setup(self):
        self.conn = mwManager.daemon_process(self, self.request)
        if not self.conn:
            self.conn = Connector(self.request, self.client_address)
        ConnectManager.add_connector(self.conn.name, self.conn.client_address, self.conn)
        logger.info('Connect From %s:%s' % self.client_address)

    def handle(self):
        error_count = 0
        try:
            while error_count < PublicConfig.ERROR_COUNT_MAX:
                info = mwManager.process(self.request, self.request.ws_recv(1024), self.func)
                if info is ERROR_FLAG:
                    error_count += 1
                elif info:
                    self.request.ws_send(info)
                else:
                    error_count += 4
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