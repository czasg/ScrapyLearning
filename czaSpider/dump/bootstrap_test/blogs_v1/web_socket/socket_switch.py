from web_socket.socket_state import *
from tools.idgen import id_pool


class Switch:

    @classmethod
    def case(cls, request, state, message, to):
        return getattr(cls, state)(request, message, to)

    @classmethod
    def w11(cls, request, message, to):
        if request.send_msg_p2g(message, 'connectors', to) is not None:
            return '%s 不存在' % to

    @classmethod
    def w12(cls, request, message, to):
        if request.send_msg_p2g(message, 'groups', to) is not None:
            return '%s 不存在' % to

    @classmethod
    def w21(cls, request, message, to):
        if ConnectManager.group_exist(to):
            return '创建失败, %s 已存在' % to
        ConnectManager.add_group(to, request.conn)

    @classmethod
    def w22(cls, request, message, to):
        if not ConnectManager.group_exist(to):
            return '加入失败, %s 不存在' % to
        ConnectManager.add_group(to, request.conn)

    @classmethod
    def w99999(cls, request, message, to):
        """Test Code"""
