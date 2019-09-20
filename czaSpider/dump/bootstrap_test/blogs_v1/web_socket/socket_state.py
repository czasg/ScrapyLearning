from collections import defaultdict

"""STATE INSTRUCTIONS
# 服务端 #
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容

# 客户端 #
11: p2p
12: p2g
21: create one group
22: add to one group

# 测试码 #
99999: return 'hello world'
"""
state_code = [11, 12, 21, 22, 99999]

ERROR_COUNT = 2


class Connector:
    def __init__(self, snow_key, request):
        self.snow_key = snow_key
        self.request = request


class ConnectManager:  # todo 加载之前就可以把所有的用户加载进来，一旦没有找到则再次更新数据库
    connectors = dict()
    groups = defaultdict(list)

    @classmethod
    def online(cls):
        return len(cls.connectors)

    @classmethod
    def clear(cls, conn):
        try:
            cls.connectors.pop(conn.snow_key)
        except:
            pass
