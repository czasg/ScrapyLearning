from collections import defaultdict
import weakref

"""STATE INSTRUCTIONS
# 服务端 #
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容

# 客户端 #
w11: p2p
w12: p2g
w21: create one group
w22: add to one group

# 测试码 #
99999: return 'hello world'
"""
state_code = ['w11', 'w12', 'w21', 'w22', 'w99999']

ERROR_COUNT = 2

KEY_MAP = {}
VAL_MAP = {}


class Connector:
    def __init__(self, snow_key, request):
        self.snow_key = snow_key
        self.request = request


class ConnectManager:  # todo 加载之前就可以把所有的用户加载进来，一旦没有找到则再次更新数据库
    connectors = defaultdict(list)
    groups = defaultdict(list)

    @classmethod
    def online(cls):
        return len(cls.connectors)

    @classmethod
    def clear(cls, conn):
        try:
            cls.connectors[conn.snow_key].pop(cls.connectors[conn.snow_key].index(conn))
        except:
            pass

    @classmethod
    def add_connector(cls, key, value):
        cls.connectors[key].append(value)

    @classmethod
    def add_group(cls, key, value):
        cls.groups[key].append(value)

    @classmethod
    def group_exist(cls, key):
        return key in cls.groups

# if __name__ == '__main__':
#     a = ConnectManager['connectors']
#     print(a)