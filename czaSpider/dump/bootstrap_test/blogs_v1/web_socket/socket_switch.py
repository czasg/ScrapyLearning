from web_socket.socket_state import *
from web_socket.socket_tools import *


class Switch:

    @classmethod
    def send_msg_p2g(cls, request, message, attr, to, **kwargs):
        if not getattr(ConnectManager, attr).get(to):
            return False
        for conn in getattr(ConnectManager, attr).get(to).values():
            try:
                conn.request.send(process_msg(message, 1, info_from=request.conn.user_name, **kwargs))
            except:
                continue

    @classmethod
    def case(cls, request, state, message, to):
        return getattr(cls, state)(request, message, to)

    @classmethod
    def w11(cls, request, message, to):
        if cls.send_msg_p2g(request, message, 'connectors', to) is not None:
            return '%s 不存在' % to

    @classmethod
    def w12(cls, request, message, to):
        if cls.send_msg_p2g(request, message, 'groups', to, group_from=to) is not None:
            return '%s 不存在' % to

    @classmethod
    def w13(cls, request, message, to):
        if cls.send_msg_p2g(request, message, 'big_home', to, group_from=to) is not None:
            return '%s 不存在' % to

    @classmethod
    def w21(cls, request, message, to):
        if ConnectManager.group_exist(to):
            return '创建失败, %s 已存在' % to
        ConnectManager.add_group(to, request.conn.client_address, request.conn)

    @classmethod
    def w22(cls, request, message, to):
        if not ConnectManager.group_exist(to):
            return '加入失败, %s 不存在' % to
        ConnectManager.add_group(to, request.conn.client_address, request.conn)

    @classmethod
    def w23(cls, request, message, to):
        ConnectManager.add_big_home(request.conn.client_address, request.conn)

    @classmethod
    def w99999(cls, request, message, to):
        """Test Code"""
