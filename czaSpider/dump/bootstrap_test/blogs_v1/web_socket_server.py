import socket
import logging
import socketserver

from web_socket.socket_error import AuthenticationError
from web_socket.socket_token_check import TokenChecker
from web_socket.socket_switch import *

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""
1176293097512894464 - test
webSocketChat.say11('asd', '1176293097512894464')
1176376872007630848 - root
webSocketChat.say11('asd', '1176376872007630848')
"""


class Socket(socket.socket):
    def __init__(self, family=-1, type=-1, proto=-1, fileno=None):
        super(Socket, self).__init__(family, type, proto, fileno)

    def accept(self):
        fd, addr = self._accept()
        sock = Socket(self.family, self.type, self.proto, fileno=fd)
        if socket.getdefaulttimeout() is None and self.gettimeout():
            sock.setblocking(True)
        return sock, addr


class MyServerThreadingMixIn(socketserver.ThreadingMixIn):
    """连接开启新线程"""


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
            path, key = WebSocketProtocol.encode(request.recv(1024))
            request.send(key)
            request.__path__ = path
        except:
            return False
        return True


class MyServerHandler(socketserver.BaseRequestHandler):

    def get_recv_data(self, size=1024):
        return WebSocketProtocol.decode(self.request.recv(size))

    def send_to_user(self, info, state, info_from='WebSocketServer', **kwargs):
        self.request.send(process_msg(info, state, ConnectManager.online(), info_from, **kwargs))

    def failure(self, info='failure', state=2):
        self.send_to_user(info, state)

    def success(self, info='success'):
        self.send_to_user(info, 1)

    def token_check(self):
        try:
            json_data = json.loads(self.get_recv_data())
            self.conn = Connector(TokenChecker.check(json_data['Cookie']), self.request, self.client_address)
            ConnectManager.add_connector(self.conn.snow_key, self.conn.client_address, self.conn)
            Switch.case(self, 'w23', '-', '-')
            return
        except:
            pass
        raise AuthenticationError

    def handle(self):
        try:
            logger.info('Connect From %s:%s' % self.client_address)
            self.token_check()
            error_count = 0
            while error_count < ERROR_COUNT:
                try:
                    user_info = json.loads(self.get_recv_data())
                    state = user_info['state']
                    message = user_info['message']
                    to = user_info['to']
                    assert state in state_code
                    info = Switch.case(self, state, message, to)
                    if info:
                        self.failure(info)
                        continue
                    self.success()
                except json.decoder.JSONDecodeError:
                    self.failure('请求数据结构异常，请传递dict')
                    error_count += 1
                except KeyError:
                    self.failure('请求参数异常，请携带state/message/to')
                    error_count += 1
                except AssertionError:
                    self.failure('state异常，不在请求范围内')
                    error_count += 1
            self.failure('错误查询次数过多，已关闭连接', 0)
        except AuthenticationError:
            logger.warning('%s:%s Authentication Failed' % self.client_address)
            self.failure('验证失败，已关闭连接', 0)
        except:
            pass

    def finish(self):
        logger.warning('%s:%s Connect Close' % self.client_address)
        try:
            ConnectManager.clear(self.conn.snow_key, self.conn.client_address)
        except:
            pass


class MyServerThreadingTCPServer(MyServerThreadingMixIn, MyServerTCPServer):

    def __init__(self, server_address, RequestHandlerClass, request_queue_size=5):
        logger.info('Server Start ...')
        logger.info('Server Address is %s:%s' % server_address)
        ProtocolProperty.set_location(server_address)
        self.request_queue_size = request_queue_size
        super(MyServerThreadingTCPServer, self).__init__(server_address, RequestHandlerClass)


def start_server(addrPort, handler=MyServerHandler, queue_size=5):
    server = MyServerThreadingTCPServer(addrPort, handler, queue_size)
    server.serve_forever()


if __name__ == '__main__':
    start_server(('127.0.0.1', 8022))

"""
监听message事件，在服务器响应时接受数据。返回的数据存储在事件对象中
ws =new WebSocket("ws://127.0.0.1:8022");
ws.onmessage = function (ev) {
    console.log(JSON.parse(ev.data));
}
ws.send(JSON.stringify({'name':'ga', 'cookie':'test', 'message':'haha', 'to':'pa', 'state': 'w11'}))
ws.send(JSON.stringify({'name':'pa', 'cookie':'test', 'message':'heihei', 'to':'ga'}))
ws.send(JSON.stringify({'name':'sf', 'cookie':'test', 'message':'heihei', 'to':'ga'}))

ws.send(JSON.stringify({'Cookie':document.cookie, 'message':'heihei', 'to':'big_home', 'state': 'w21'}))

监听open事件，在成功建立websocket时向url发送纯文本字符串数据
websocket.onopen = () => {
  if (websocket.readyState === WebSocket.OPEN) {
    websocket.send('hello world')
  }
}
"""
