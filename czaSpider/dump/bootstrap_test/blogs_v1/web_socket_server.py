import logging
import socketserver

from web_socket.socket_error import AuthenticationError
from web_socket.socket_state import *
from web_socket.socket_tools import *
from tools.idgen import id_pool

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class MyServerHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.request.send(socket_encode(self.request.recv(1024)))

    def send_to_user(self, info, state, info_from='WebSocketServer'):  # 自己用的
        self.request.send(process_msg(info, state, ConnectManager.online(), info_from))

    def get_recv_data(self, size=1024):
        return socket_decode(self.request.recv(size))

    def success(self, info='success'):
        self.send_to_user(info, 1)

    def failure(self, info='failure', state=2):
        self.send_to_user(info, state)

    def token_check(self):
        try:
            json_data = json.loads(self.get_recv_data())
            if json_data['cookie'] == 'test':  # todo Cookie验证
                self.conn = Connector(json_data['name'], self.request)  # id_pool.next_id()
                ConnectManager.add_connector(json_data['name'], self.conn)
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
                except KeyError:
                    self.failure('请求参数异常，请携带state/message/to')
                    error_count += 1
                    continue
                except AssertionError:
                    self.failure('state异常，不在请求范围内')
                    error_count += 1
                    continue
                if state == 11:
                    if self.send_msg_p2g(message, 'connectors', to):
                        pass
                    else:
                        self.failure('%s 不存在' % to)
                        continue
                elif state == 12:
                    if self.send_msg_p2g(message, 'groups', to):
                        pass
                    else:
                        self.failure('%s 不存在' % to)
                        continue
                elif state == 21:
                    if ConnectManager.group_exist(to):
                        self.failure('%s 已存在' % to)
                        continue
                    else:
                        ConnectManager.add_group(to, self.conn)
                elif state == 22:  # todo 用户加进去了怎么删除啊，懵逼了，哈哈
                    if ConnectManager.group_exist(to):
                        ConnectManager.add_group(to, self.conn)
                    else:
                        self.failure('%s 不存在' % to)
                        continue
                elif state == 99999:
                    pass
                self.success()
            self.failure('错误查询次数过多，已关闭连接', 0)
        except AuthenticationError:
            logger.warning('%s:%s Authentication Failed' % self.client_address)
            self.failure('验证失败，已关闭连接', 0)
        except:
            pass

    def send_msg_p2g(self, message, attr, to):
        if getattr(ConnectManager, attr).get(to):
            for conn in getattr(ConnectManager, attr).get(to):
                conn.request.send(process_msg(message, 1, info_from=self.conn.snow_key))
            return True
        else:
            return False

    def finish(self):
        logger.warning('%s:%s Connect Close' % self.client_address)
        ConnectManager.clear(self.conn)


class MyServerThreadingTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, request_queue_size=5):
        logger.info('Server Start ...')
        logger.info('Server Address is %s:%s' % server_address)
        self.request_queue_size = request_queue_size
        super(MyServerThreadingTCPServer, self).__init__(server_address, RequestHandlerClass)


if __name__ == '__main__':
    server = MyServerThreadingTCPServer(('127.0.0.1', 8022), MyServerHandler, 500)
    server.serve_forever()

    """
    ws =new WebSocket("ws://127.0.0.1:8022");
    ws.onmessage = function (ev) {
        console.log(JSON.parse(ev.data));
    }
    ws.send(JSON.stringify({'name':'ga', 'cookie':'test', 'message':'haha', 'to':'pa', 'state': 11}))
    ws.send(JSON.stringify({'name':'pa', 'cookie':'test', 'message':'heihei', 'to':'ga'}))
    ws.send(JSON.stringify({'name':'sf', 'cookie':'test', 'message':'heihei', 'to':'ga'}))
    """
