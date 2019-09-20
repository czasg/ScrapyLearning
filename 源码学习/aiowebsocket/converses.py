import asyncio
import logging
from asyncio import Queue

from .freams import Frames
from .enumerations import SocketState, ControlFrames, DataFrames
from .handshakes import HandShake
from .parts import parse_uri


class AioWebSocket:
    def __init__(self, uri: str, headers: list,
                 union_header: dict, timeout: int = 30,
                 read_timeout: int = 120):
        self.uri = uri
        self.hands = None
        self.reader = None
        self.writer = None
        self.converse = None
        self.timeout = timeout
        self.read_timeout = read_timeout
        self.headers = headers
        self.union_header = union_header
        self.state = SocketState.zero.value  # 通过这个状态码对连接进行开关

    async def close_connection(self):
        if self.state is SocketState.closed.value:
            raise ConnectionError('SocketState is closed, can not close.')
        if self.state is SocketState.closing:
            logging.warning('SocketState is closing')
        await self.converse.send(message=b'')  # 通过对converse发送一个空的二进制字符串就会关闭整个连接吗

    async def create_connection(self):
        if self.state is not SocketState.zero.value:
            raise ConnectionError('Connection is already exists.')
        remote = scheme, host, port, resource, ssl = parse_uri(self.uri)
        reader, writer = await asyncio.open_connection(host=host, port=port, ssl=ssl)  # 这是啥，asyncio自带的连接嘛
        self.reader = reader  # 通过asyncio.open_connection获取读写两个句柄嘛
        self.writer = writer
        self.hands = HandShake(remote, reader, writer,
                               headers=self.headers,
                               union_header=self.union_header)
        await self.hands.shake_()
        status_code = await self.hands.shake_result()  # 这两步感觉是类似http协议的握手环节啊，只需要一次握手就可以了
        if status_code is not 101:
            raise ConnectionError('Connection failed,status code:{code}'.format(code=status_code))
        self.converse = Converse(reader, writer)  # 通过读写两个句柄创建 操作框
        self.state = SocketState.opened.value  # 修改当前状态码

    @property
    def manipulator(self):
        return self.converse

    async def __aenter__(self):  # 原来玩意是当使用async with的时候回执行一次的啊，好吧
        create = asyncio.wait_for(self.create_connection(), timeout=self.timeout)  # 我去，这个wait_for有点意思啊
        try:
            await create  # 执行create_connection函数进行创造Converse对象
        except asyncio.TimeoutError as exc:
            raise ConnectionError('Connection time out,exc:{exc}'.format(exc=exc))
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close_connection()


class Converse:
    def __init__(self, reader: object, writer: object, maxsize: int = 2**16):
        self.reader = reader
        self.writer = writer
        self.message_queue = Queue(maxsize=maxsize)  # 接收消息直接从这里get就可以了
        self.frame = Frames(self.reader, self.writer)  # 帧  写/发送消息的操作在这里

    async def send(self, message,
                   fin: bool = True, mask: bool = True):  # 发送消息
        if isinstance(message, str):
            message = message.encode()
        code = DataFrames.text.value  # 0x01
        await self.frame.write(fin=fin, code=code, message=message, mask=mask)

    async def receive(self, text=False, mask=False):  # 接收消息
        if not self.message_queue.qsize():
            single_message = await self.frame.read(text, mask)
            await self.message_queue.put(single_message)
        message = await self.message_queue.get()  # 当异步队列存在的时候，使用get方法获取其中的消息
        return message or None

    @property
    def get_queue_size(self):  # 获取异步队列的大小
        return self.message_queue.qsize()
