from web_socket.socket_state import *
from web_socket.socket_tools import *
from database.redis.database_redis import redis_handler, REDIS_USER_SNOW_ID
from database.mongodb.database_mongodb import mongodb_handler

"""STATE INSTRUCTIONS
### 服务端 ###
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容

### 客户端 ###
w11: p2p
w12: p2g
w13:
w21: create new group
w22: add in one group
w23: -User Forbidden- add in big home
w31: search unread msg from database cache

### 测试码 ###
w99999: do nothing, you can use it to ShakeHands
"""
state_code = ['w11', 'w12', 'w13', 'w21', 'w22', 'w23', 'w31', 'w99999']


class Switch:

    @classmethod
    def send_msg_p2a(cls, request, message, attr, to, save=False, **kwargs):
        online_socket = getattr(ConnectManager, attr).get(to)
        if online_socket:
            for conn in online_socket.values():
                try:
                    conn.request.send(process_msg(message, 1, info_from=request.conn.user_name, **kwargs))
                    mongodb_handler.insert_mongodb(attr, request.conn.snow_key, to, message, state=1,
                                                   fromUserName=request.conn.user_name) if save else None
                except:
                    continue
        elif save:
            mongodb_handler.insert_mongodb(attr, request.conn.snow_key, to, message, state=0,
                                           fromUserName=request.conn.user_name)
        else:
            return False

    @classmethod
    def send_unread_msg(cls, request, unread):
        request.request.send(process_msg(unread, 1, info_from='WebSocketServerCache'))

    @classmethod
    def case(cls, request, state, message, to):
        if request.conn.snow_key == to:
            return '%s 不能和自己聊天咯' % to
        return getattr(cls, state)(request, message, to)

    @classmethod
    def w11(cls, request, message, to):  # pass
        if not redis_handler.hexists(REDIS_USER_SNOW_ID, to):
            return '%s 不存在' % to
        cls.send_msg_p2a(request, message, 'connectors', to, save=True)

    @classmethod
    def w12(cls, request, message, to):  # pass
        if not ConnectManager.groups.get(to):
            return '%s 不存在' % to
        if request.conn not in ConnectManager.groups.get(to).values():
            return '%s 你不在此群组内，无法聊天' % to
        cls.send_msg_p2a(request, message, 'groups', to, group_from=to)

    @classmethod
    def w13(cls, request, message, to):  # pass
        cls.send_msg_p2a(request, message, 'big_home', 'big_home', group_from=to)

    @classmethod
    def w21(cls, request, message, to):  # pass
        if ConnectManager.group_exist(to):
            return '创建失败, %s 已存在' % to
        ConnectManager.add_group(to, request.conn.client_address, request.conn)

    @classmethod
    def w22(cls, request, message, to):  # pass
        if not ConnectManager.group_exist(to):
            return '加入失败, %s 不存在' % to
        ConnectManager.add_group(to, request.conn.client_address, request.conn)

    @classmethod
    def w23(cls, request, message, to):  # pass
        ConnectManager.add_big_home(request.conn.client_address, request.conn)

    @classmethod
    def w31(cls, request, message, to):
        unread = []
        for attr in ['connectors', 'groups']:
            unread.extend(list(mongodb_handler.client[attr][request.conn.snow_key].find({'state': 0}, {"_id": 0})))
            mongodb_handler.client[attr][request.conn.snow_key].update_many({}, {"$set": {"state": 1}})
        if unread:
            cls.send_unread_msg(request, unread)

    @classmethod
    def w99999(cls, request, message, to):
        """Test Code"""
