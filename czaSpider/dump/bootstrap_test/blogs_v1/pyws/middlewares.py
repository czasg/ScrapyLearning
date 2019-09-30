import json

from collections import deque
from collections.abc import Iterable

from pyws.protocol import WebSocketProtocol
from pyws.errors import *
from pyws.connector import Connector, ConnectManager


class BaseMiddleware:

    @classmethod
    def process_input(self, input): return input

    @classmethod
    def process_output(self, output): return output


class DaemonMiddleware(BaseMiddleware):
    """在整个流程中有一次起作用"""

    @classmethod
    def process_output(cls, output_msg):
        if isinstance(output_msg, (str, dict, list)):
            return WebSocketProtocol.encode_msg(json.dumps(output_msg, ensure_ascii=False).encode('utf-8'))
        else:
            raise OutputTypeError


class DataMiddleware(BaseMiddleware):
    """数据流程执行的中间件"""


class WSMiddleware(DataMiddleware):

    @classmethod
    def process_input(self, input_msg):
        return WebSocketProtocol.decode_msg(input_msg)

    @classmethod
    def process_output(cls, output_msg):
        if isinstance(output_msg, (str, dict, list)):
            return WebSocketProtocol.encode_msg(json.dumps(output_msg, ensure_ascii=False).encode('utf-8'))
        else:
            raise OutputTypeError


class MiddlewareManager:
    """
    这个中间件的输入，首先会被第一道中间件给处理，以便获取最初的数据
    最后处理的是也是这个中间件，会将数据润色，能够直接send出去的那种
    """
    daemon_middleware = {
        'process_input': deque(),
        'process_output': deque(),
    }
    data_middleware = {
        'process_input': deque(),
        'process_output': deque(),
    }
    daemon_middleware_count = 0
    data_middleware_count = 0

    def __init__(self):
        self.add_middleware(WSMiddleware)

    @classmethod
    def check_base(cls, middleware):
        if isinstance(middleware, DaemonMiddleware):
            middle_type = 0
        elif isinstance(middleware, DataMiddleware):
            middle_type = 1
        else:
            raise MiddlewareError
        return middle_type

    @classmethod
    def add_middleware(cls, middleware=None):
        if isinstance(middleware, type):
            middleware = middleware()
        if middleware:
            if cls.check_base(middleware):
                cls.data_middleware_count += 1
                cls._add_middleware('data_middleware', middleware)
            else:
                cls.daemon_middleware_count += 1
                cls._add_middleware('daemon_middleware', middleware)

    @classmethod
    def _add_middleware(cls, attr, middleware):
        getattr(cls, attr)['process_input'].append(getattr(middleware, 'process_input'))
        getattr(cls, attr)['process_output'].appendleft(getattr(middleware, 'process_output'))

    @classmethod
    def add_middlewares(cls, middlewares=None):
        if middlewares and isinstance(middlewares, Iterable):
            for middleware in middlewares:
                cls.add_middleware(middleware)

    @classmethod
    def auto_add(cls, middle):
        if isinstance(middle, Iterable):
            cls.add_middlewares(middle)
        else:
            cls.add_middleware(middle)

    @classmethod
    def process(cls, request, data, func=None):
        for process_input in cls.data_middleware['process_input']:
            data = process_input(data)
        # print(type(data), data, 'middleware')
        data = func(request, data) if func else data
        if data:  # 函数如果有返回，就是默认走OK，相当于那边的success
            # print('这应该是没有问题的')
            for process_output in cls.data_middleware['process_output']:
                data = process_output(data)
        # print(data)
        return data  # 我感觉这里很重要，这里就是我们常用的那种

    @classmethod
    def daemon_process(cls, handler, request):
        try:
            if cls.daemon_middleware_count:
                data = WebSocketProtocol.decode_msg(request.recv(1024))
                for process_input in cls.daemon_middleware['process_input']:
                    data = process_input(data)
                for process_output in cls.daemon_middleware['process_output']:
                    data = process_output(data)
                return Connector(request, handler.client_address, data)
        except:
            raise AuthenticationError


mwManager = MiddlewareManager()

if __name__ == '__main__':
    mwManager.auto_add(DaemonMiddleware)
    print(mwManager.daemon_middleware_count)
    print(mwManager.data_middleware_count)
