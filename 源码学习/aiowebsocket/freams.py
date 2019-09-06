import io
import random
import logging
from struct import pack, unpack
from itertools import cycle
from .enumerations import *
from .exceptions import FrameError


class Frames:
    """数据帧相关操作"""
    def __init__(self, reader: object, writer: object):
        self.reader = reader
        self.writer = writer
        self.maxsize = 2**64

    @staticmethod
    def message_mask(message: bytes, mask):
        if len(mask) != 4:
            raise FrameError("The 'mask' must contain 4 bytes")
        return bytes(b ^ m for b, m in zip(message, cycle(mask)))

    async def pong(self, message: bytes = b''):
        await self.write(fin=True, code=ControlFrames.pong.value, message=message)

    async def extra_operation(self, code: int, message: bytes):
        if code not in DataFrames._value2member_map_:
            if code is ControlFrames.ping.value:
                await self.pong(message=message)
            elif code is ControlFrames.close.value:
                await self.receive_close()
            else:
                raise FrameError('Invalid operation code.')

    async def unpack_frame(self, mask=False, maxsize=None):
        reader = self.reader.readexactly
        frame_header = await reader(2)
        head1, head2 = unpack('!BB', frame_header)

        fin = True if head1 & 0b10000000 else False
        rsv1 = True if head1 & 0b01000000 else False
        rsv2 = True if head1 & 0b00100000 else False
        rsv3 = True if head1 & 0b00010000 else False
        code = head1 & 0b00001111

        if (True if head2 & 0b10000000 else False) != mask:
            raise FrameError("Incorrect masking")

        length = head2 & 0b01111111
        if length == 126:
            message = await reader(2)
            length, = unpack('!H', message)
        elif length == 127:
            message = await reader(8)
            length, = unpack('!Q', message)
        if maxsize and length > maxsize:
            raise FrameError("Message length is too long)".format(length, maxsize))
        if mask:
            mask_bits = await reader(4)
        message = self.message_mask(message, mask_bits) if mask else await reader(length)
        return fin, code, rsv1, rsv2, rsv3, message

    async def read(self, text=False, mask=False, maxsize=None):
        """return information about message
        """
        fin, code, rsv1, rsv2, rsv3, message = await self.unpack_frame(mask, maxsize)
        await self.extra_operation(code, message)  # 根据操作码决定后续操作
        if any([rsv1, rsv2, rsv3]):
            logging.warning('RSV not 0')
        if not fin:
            logging.warning('Fragmented control frame:Not FIN')
        if code is DataFrames.binary.value and text:
            if isinstance(message, bytes):
                message = message.decode()
        if code is DataFrames.text.value and not text:
            if isinstance(message, str):
                message = message.encode()
        return message

    @staticmethod
    def pack_message(fin, code, mask, rsv1=0, rsv2=0, rsv3=0):
        head1 = (
                (0b10000000 if fin else 0)
                | (0b01000000 if rsv1 else 0)
                | (0b00100000 if rsv2 else 0)
                | (0b00010000 if rsv3 else 0)
                | code
        )
        head2 = 0b10000000 if mask else 0  # Whether to mask or not
        return head1, head2

    async def write(self, fin, code, message, mask=True, rsv1=0, rsv2=0, rsv3=0):
        head1, head2 = self.pack_message(fin, code, mask, rsv1, rsv2, rsv3)
        output = io.BytesIO()
        length = len(message)
        if length < 126:
            output.write(pack('!BB', head1, head2 | length))
        elif length < 2**16:
            output.write(pack('!BBH', head1, head2 | 126, length))
        elif length < 2**64:
            output.write(pack('!BBQ', head1, head2 | 127, length))
        else:
            raise ValueError('Message is too long')

        if mask:
            mask_bits = pack('!I', random.getrandbits(32))
            output.write(mask_bits)
            message = self.message_mask(message, mask_bits)

        output.write(message)
        self.writer.write(output.getvalue())

    async def receive_close(self):...
