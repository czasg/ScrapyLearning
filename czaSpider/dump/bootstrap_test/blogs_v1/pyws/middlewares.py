from collections import deque
from collections.abc import Iterable

from pyws.public import *
from pyws.connector import Connector


class BaseMiddleware:

    @classmethod
    def process_input(cls, request, input_msg): return input_msg

    @classmethod
    def process_output(cls, request, output_msg): return output_msg


class CircleMiddleware:  # todo, 可以在此处加一个在主线程就挂起的循环，不过这玩意用线程不知道怎么样，应该也还行把
    data = None

    @classmethod
    def process_data(cls):
        cls.data = None


class DaemonMiddleware(BaseMiddleware):
    """在整个流程中有一次起作用"""


class DataMiddleware(BaseMiddleware):
    """数据流程执行的中间件"""


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
    def _add_middleware(cls, attr, middleware):
        getattr(cls, attr)['process_input'].append(getattr(middleware, 'process_input'))
        getattr(cls, attr)['process_output'].appendleft(getattr(middleware, 'process_output'))

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
        try:
            for process_input in cls.data_middleware['process_input']:
                data = process_input(request, data)
            data = (func(request, data) if func else data) or PublicConfig.DEFAULT_REPLY
            for process_output in cls.data_middleware['process_output']:
                data = process_output(request, data)
            return data
        except DataMiddlewareAbnormal:
            return ERROR_FLAG

    @classmethod
    def daemon_process(cls, handler, request):
        try:
            if cls.daemon_middleware_count:
                data = request.ws_recv(1024)
                for process_input in cls.daemon_middleware['process_input']:
                    data = process_input(request, data)
                for process_output in cls.daemon_middleware['process_output']:
                    data = process_output(request, data)
                return Connector(request, handler.client_address, data)
        except:
            raise AuthenticationError


mwManager = MiddlewareManager()

if __name__ == '__main__':
    mwManager.auto_add(DaemonMiddleware)
    print(mwManager.daemon_middleware_count)
    print(mwManager.data_middleware_count)
