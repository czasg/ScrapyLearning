import socketserver, logging, json, base64, hashlib, struct

from collections import defaultdict

from socket_error import AuthenticationError
from socket_state import state_code
from socket_tools import process_msg, socket_encode, socket_decode

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class Connector:
    def __init__(self, snow_key, obj, address_port):
        self.snow_key = snow_key
        self.obj = obj
        self.address_port = address_port


class Groups:
    groups = defaultdict(list)

    def is_empty(self):
        return len(self.groups) == 0


class MyServerHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.request.send(socket_encode(self.request.recv(1024)))

    def send_to_user(self, info, state):  # 自己用的
        self.request.send(process_msg(info, state))

    def get_recv_data(self, size=1024):
        return socket_decode(self.request.recv(size))

    def token_check(self):
        try:
            json_data = json.loads(self.get_recv_data())
            if json_data['cookie'] == 'test':
                connector[json_data['name']] = self.request
                return
        except ConnectionResetError:
            raise ConnectionResetError
        except:
            pass
        raise AuthenticationError

    def handle(self):
        global connector
        try:
            logger.info('Connect From %s:%s' % self.client_address)
            self.token_check()
            error_count = 0
            while error_count < 10:
                try:
                    user_info = json.loads(self.get_recv_data())
                    state = user_info['state']
                    message = user_info['message']
                    assert state in state_code
                except KeyError:
                    self.send_to_user('请求参数异常，请携带state/message', 2)
                    error_count += 1
                    continue
                except AssertionError:
                    self.send_to_user('state异常，不在请求范围内', 2)
                    error_count += 1
                    continue
                if state == 11:
                    to_obj = connector.get(user_info['to'])
                    if to_obj:
                        to_obj.send(process_msg(message, 1))
                        self.send_to_user('发送成功', 1) if user_info.get('feedback') else None
                    else:
                        self.send_to_user('无此用户耶', 2)
                elif state == 12:
                    self.send_to_user(message, 1)
                elif state == 99999:
                    self.send_to_user('hello world', 1)

            self.send_to_user('错误查询次数过多，已关闭连接', 0)
        except AuthenticationError:
            logger.warning('%s:%s Authentication Failed' % self.client_address)
            self.send_to_user('验证失败，已关闭连接', 0)
        except:
            pass

    def finish(self):
        logger.warning('%s:%s Connect Close' % self.client_address)


class MyServerThreadingTCPServer(socketserver.ThreadingTCPServer):

    def __init__(self, server_address, RequestHandlerClass, request_queue_size=5):
        logger.info('Server Start ...')
        logger.info('Server Address is %s:%s' % server_address)
        self.request_queue_size = request_queue_size
        super(MyServerThreadingTCPServer, self).__init__(server_address, RequestHandlerClass)


if __name__ == '__main__':
    server = MyServerThreadingTCPServer(('127.0.0.1', 8022), MyServerHandler, 500)
    server.serve_forever()
