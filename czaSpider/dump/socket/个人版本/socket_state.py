state_code = [0, 1, 2, 11, 99999]
"""STATE INSTRUCTIONS

# 服务端 #
0: 关闭连接，具体原因见返回内容
1: 请求成功
2: 错误状态，具体原因见返回内容

# 客户端 #
11: p2p

# 测试码 #
99999: return 'hello world'

"""
