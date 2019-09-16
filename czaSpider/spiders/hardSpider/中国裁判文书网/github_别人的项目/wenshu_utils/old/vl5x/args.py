import hashlib
import random
from typing import Union

from . import _vl5x


class Vjkl5(str):

    def __new__(cls):
        return super(Vjkl5, cls).__new__(cls, hashlib.sha1(str(random.random()).encode()).hexdigest())


class Vl5x(str):

    def __new__(cls, vjkl5: Union[Vjkl5, str]):
        return super(Vl5x, cls).__new__(cls, _vl5x.get_vl5x(vjkl5))


class Number(str):

    def __new__(cls):
        return super(Number, cls).__new__(cls, "{:.2f}".format(random.random()))


class Guid(str):

    def __new__(cls):
        return super(Guid, cls).__new__(cls, cls.__get_guid())

    @classmethod
    def __get_guid(cls) -> str:
        return "{}{}-{}-{}{}-{}{}{}".format(
            cls.__create_guid(), cls.__create_guid(),
            cls.__create_guid(), cls.__create_guid(),
            cls.__create_guid(), cls.__create_guid(),
            cls.__create_guid(), cls.__create_guid(),
        )

    @staticmethod
    def __create_guid() -> str:
        return hex(int((1 + random.random()) * 0x10000) | 0)[3:]
