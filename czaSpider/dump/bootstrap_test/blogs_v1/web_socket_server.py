import logging
import socketserver

from web_socket.socket_error import AuthenticationError
from web_socket.socket_token_check import TokenChecker
from web_socket.socket_tools import *
from web_socket.socket_switch import *

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MyServerHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.request.send(WebSocketProtocol.encode(self.request.recv(1024)))

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
            import traceback
            logging.error(traceback.format_exc())
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
            import traceback
            print(traceback.format_exc())
            self.failure('验证失败，已关闭连接', 0)
        except:
            pass

    def finish(self):
        logger.warning('%s:%s Connect Close' % self.client_address)
        ConnectManager.clear(self.conn.snow_key, self.conn.client_address)


class MyServerThreadingTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, request_queue_size=5):
        logger.info('Server Start ...')
        logger.info('Server Address is %s:%s' % server_address)
        ProtocolProperty.set_location(server_address)
        self.request_queue_size = request_queue_size
        super(MyServerThreadingTCPServer, self).__init__(server_address, RequestHandlerClass)


def start_server(addrPort, handler=MyServerHandler, queue_size=500):
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
