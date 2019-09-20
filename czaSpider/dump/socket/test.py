import socketserver, logging, json, base64, hashlib, struct
def jm(data):
    def get_headers(data):
        '''将请求头转换为字典'''
        header_dict = {}
        print(data)
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
logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

"""state
# 服务端 #
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容

# 客服端 #
11: 表示点对点聊天
"""
def get_headers(data):
    '''将请求头转换为字典'''
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
    # 这个倒是没见过，只知道有一个byteIO，原来还有一耳光list额类型呀
    bytes_list = bytearray()  # 这里我们使用字节将数据全部收集，再去字符串编码，这样不会导致中文乱码
    for i in range(len(decoded)):
        chunk = decoded[i] ^ mask[i % 4]  # 解码方式
        bytes_list.append(chunk)
    body = str(bytes_list, encoding='utf-8')
    return body
def send_msg(conn, msg_bytes):
    """
    WebSocket服务端向客户端发送消息
    :param conn: 客户端连接到服务器端的socket对象,即： conn,address = socket.accept()
    :param msg_bytes: 向客户端发送的字节
    :return:
    """
    import struct

    token = b"\x81"  # 接收的第一字节，一般都是x81不变
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg_bytes
    conn.send(msg)
    return True
# 对请求头中的sec-websocket-key进行加密
response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
               "Upgrade:websocket\r\n" \
               "Connection: Upgrade\r\n" \
               "Sec-WebSocket-Accept: %s\r\n" \
               "WebSocket-Location: ws://%s%s\r\n\r\n"
magic_string = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'


class AuthenticationError(Exception): ...


def to_user(content, state):
    return json.dumps({'state': state, 'content': content}).encode()


class Connector:
    def __init__(self, obj):
        self.obj = obj


class Group:
    pass

connector = {}
class MyServerHandler(socketserver.BaseRequestHandler):

    def send_to_user(self, info, state):
        token = b"\x81"  # 接收的第一字节，一般都是x81不变
        msg_bytes = to_user(info, state)
        length = len(msg_bytes)
        if length < 126:
            token += struct.pack("B", length)
        elif length <= 0xFFFF:
            token += struct.pack("!BH", 126, length)
        else:
            token += struct.pack("!BQ", 127, length)
        msg = token + msg_bytes
        self.request.send(msg)
        # self.request.send(to_user(info, state))

    def token_check(self):
        global connector

        token = self.request.recv(1024)
        headers = get_headers(token)
        value = headers['Sec-WebSocket-Key'] + magic_string
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (ac.decode('utf-8'), headers['Host'], headers['url'])
        self.request.send(bytes(response_str, encoding='utf-8'))
        # try:
        #     json_data = json.loads(token)
        #     if json_data['cookie'] == 'test':
        #         self.send_to_user('验证成功', 1)
        #         connector[json_data['user']] = Connector(self.request)
        #         return
        # except ConnectionResetError:
        #     raise ConnectionResetError
        # raise AuthenticationError

    def handle(self):
        global connector
        try:
            logger.info('Connect From %s:%s' % self.client_address)
            self.token_check()
            error_count = 0
            while error_count < 10:
                user_info = self.request.recv(1024)  # 进来就是等待用户的消息，只要有问题就continue过来
                try:
                    user_info = json.loads(get_data(user_info))
                    state = user_info['state']
                    assert state in [0, 1, 2, 11]
                except:
                    self.send_to_user('参数有误，需要携带具体状态state', 2)
                    error_count += 1
                    continue
                if state == 11:
                    obj = connector.get(user_info['to'])
                    if obj:
                        obj.obj.send(to_user(user_info['message'], 1))
                        self.send_to_user('发送成功', 1)
                    else:
                        self.send_to_user('无此用户耶', 2)

            self.send_to_user('错误查询次数过多，已关闭连接', 0)
        except ConnectionResetError:
            pass
        except AuthenticationError:
            logger.warning('%s:%s Authentication Failed' % self.client_address)
            self.send_to_user('验证失败，已关闭连接', 0)

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
