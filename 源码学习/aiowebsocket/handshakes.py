import re
import random
import base64

from .exceptions import HandShakeError

_value_re = re.compile(rb"[\x09\x20-\x7e\x80-\xff]*")


class HandShake:
    def __init__(self, remote, reader, writer, headers, union_header):
        self.remote = remote
        self.write = writer
        self.reader = reader
        self.headers = headers
        self.union_header = union_header

    def shake_headers(self, host: str, port: int, resource: str = '/',
                      version: int = 13):  # 为请求添加请求头
        if self.headers:
            if isinstance(self.headers, list):
                return '\r\n'.join(self.headers) + '\r\n'
            if isinstance(self.headers, dict):
                head = ['{}:{}'.format(k, item) for k, item in self.headers.items()]
                return '\r\n'.join(head) + '\r\n'

        bytes_key = bytes(random.getrandbits(8) for _ in range(16))
        key = base64.b64encode(bytes_key).decode()
        head = {'Host': '{host}:{port}'.format(host=host, port=port),
                'Connection': 'Upgrade',
                'Upgrade': 'websocket',
                'User-Agent': 'Python/3.7',
                'Origin': 'http://{host}'.format(host=host),
                'Sec-WebSocket-Key': key,
                'Sec-WebSocket-Version': version
                }
        for u, i in self.union_header.items():
            head[u] = i
        headers = ['{}:{}'.format(k, item) for k, item in head.items()]
        headers.insert(0, 'GET {} HTTP/1.1'.format(resource))
        headers.append('\r\n')
        return '\r\n'.join(headers)

    async def shake_(self):  # 1
        """Initiate a handshake"""
        porn, host, port, resource, ssl = self.remote
        handshake_info = self.shake_headers(host=host, port=port,
                                            resource=resource)
        self.write.write(data=handshake_info.encode())  # 写之前需要创建一些先行条件，就是这里吗

    async def shake_result(self):  # 2
        header = []
        for _ in range(2 ** 8):  # 使用位移算法 256
            result = await self.reader.readline()  # 在写之后立即读一些东西吗
            header.append(result)
            if result == b'\r\n':
                break
        if not header:
            raise HandShakeError('HandShake not response')
        protocols, socket_code = header[0].decode('utf-8').split()[:2]
        if protocols != "HTTP/1.1":
            raise HandShakeError("Unsupported HTTP version: %r" % protocols)
        socket_code = int(socket_code)
        if not 100 <= socket_code < 1000:
            raise HandShakeError("Unsupported HTTP status code: %d" % socket_code)
        return socket_code
