import json, base64, hashlib, struct, re

from web_socket.socket_error import WebSocketProtocolError


class ProtocolProperty:
    LOCATION = None
    MAGIC_STRING = '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
    REGEX = re.compile(r'GET\s+([^\s]+).*Sec-WebSocket-Key:\s*(.*?)\r\n', re.S)
    RESPONSE_TEMPLATE = "HTTP/1.1 101 Switching Protocols\r\n" \
                        "Upgrade:websocket\r\n" \
                        "Connection: Upgrade\r\n" \
                        "Sec-WebSocket-Accept: %s\r\n" \
                        "WebSocket-Location: ws://{location}\r\n\r\n"

    @classmethod
    def set_location(cls, location):
        cls.LOCATION = '%s:%s/' % location
        cls.RESPONSE_TEMPLATE = cls.RESPONSE_TEMPLATE.format(location=cls.LOCATION)


class WebSocketProtocol(ProtocolProperty):

    @classmethod
    def check_header(cls, headers):
        try:
            path, key = cls.REGEX.search(headers).groups()
            if all((path, key)):
                return path, key
        except:
            pass
        raise WebSocketProtocolError

    @classmethod
    def get_ac_str(cls, data):
        path, value = cls.check_header(str(data, encoding="utf-8"))
        return path, base64.b64encode(hashlib.sha1((value + cls.MAGIC_STRING).encode('utf-8')).digest()).decode('utf-8')

    @classmethod
    def encode(cls, data):
        path, key = cls.get_ac_str(data)
        return path, bytes(cls.RESPONSE_TEMPLATE % key, encoding='utf-8')

    @classmethod
    def decode(cls, data):
        payload_len = data[1] & 0b1111111
        if payload_len is 0b1111110:
            mask = data[4:8]
            decoded = data[8:]
        elif payload_len is 0b1111111:
            mask = data[10:14]
            decoded = data[14:]
        else:
            mask = data[2:6]
            decoded = data[6:]
        return str(bytearray([decoded[i] ^ mask[i % 4] for i in range(len(decoded))]), encoding='utf-8')


def get_send_msg(msg_bytes, token=b"\x81"):
    length = len(msg_bytes)
    if length < 0b1111110:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)
    return token + msg_bytes


def to_user(content, state, online=1, info_from='WebSocketServer', **kwargs):
    info = {
        'state': state,
        'content': content,
        'online': online,
        'info_from': info_from
    }
    info.update(kwargs)
    return json.dumps(info, ensure_ascii=False).encode()


def process_msg(info, state, online=1, info_from='WebSocketServer', **kwargs):
    return get_send_msg(to_user(info, state, online, info_from, **kwargs))
