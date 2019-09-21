import json, base64, hashlib, struct


def socket_encode(data):
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


def socket_decode(info):
    payload_len = info[1] & 0b1111111
    if payload_len == 126:
        mask = info[4:8]
        decoded = info[8:]
    elif payload_len == 127:
        mask = info[10:14]
        decoded = info[14:]
    else:
        mask = info[2:6]
        decoded = info[6:]
    return str(bytearray([decoded[i] ^ mask[i % 4] for i in range(len(decoded))]), encoding='utf-8')  # todo, 有bug


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


def to_user(content, state, online=1, info_from='WebSocketServer'):  # todo 怎么动态添加参数，这是个大问题啊
    return json.dumps({
        'state': state,
        'content': content,
        'online': online,
        'info_from': info_from
    }).encode()


def process_msg(info, state, online=1, info_from='WebSocketServer'):
    return get_send_msg(to_user(info, state, online, info_from))
