import socketserver, logging, json, base64, hashlib, struct

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""state
# 服务端 #
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容
3: 


# 客服端 #
11: 表示点对点聊天

# 测试码 #
99999
"""
state_code = [0, 1, 2, 11, 99999]


def jm(data):
    def get_headers(data):
        header_dict = {}
        data = str(data, encoding="utf-8")
        header, body = data.split("\r\n\r\n", 1)
        header_list = header.split("\r\n")
        for i in range(0, len(header_list)):
            if i == 0:
                if len(header_list[0].split(" ")) == 3:
                    header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[0].split(" ")
            else:
                k, v = header_list[i].split(":", 1)
                header_dict[k] = v.strip()
        return header_dict

    headers = get_headers(data)
    response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                   "Upgrade:websocket\r\n" \
                   "Connection: Upgrade\r\n" \
                   "Sec-WebSocket-Accept: %s\r\n" \
                   "WebSocket-Location: ws://%s%s\r\n\r\n"
    magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    value = headers['Sec-WebSocket-Key'] + magic_string
    ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
    response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
    return bytes(response_str, encoding='utf-8')


def get_data(info):  # 这里解码的方式，不会就是那一坨完全看不懂的东西把
    payload_len = info[1] & 127
    if payload_len == 126:
        extend_payload_len = info[2:4]
        mask = info[4:8]
        decoded = info[8:]
    elif payload_len == 127:
        extend_payload_len = info[2:10]
        mask = info[10:14]
        decoded = info[14:]
    else:
        extend_payload_len = None
        mask = info[2:6]
        decoded = info[6:]
    bytes_list = bytearray()
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    return body


def get_send_msg(msg_bytes):
    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
    msg = token + msg_bytes
    return msg


def to_user(content, state):
    return json.dumps({'state': state, 'content': content}).encode()


def process_msg(info, state):
    return get_send_msg(to_user(info, state))


class AuthenticationError(Exception): ...


class Connector:
    def __init__(self, obj):
        self.obj = obj


class Group:
    pass


connector = {}


class MyServerHandler(socketserver.BaseRequestHandler):

    def setup(self):
        self.request.send(jm(self.request.recv(1024)))

    def send_to_user(self, info, state):
        self.request.send(process_msg(info, state))

    def get_recv_data(self, size=1024):
        return get_data(self.request.recv(size))

    def token_check(self):
        global connector
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
