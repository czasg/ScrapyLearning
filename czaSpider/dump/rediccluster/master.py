from rediscluster import StrictRedisCluster
# todo. redis cluster environment
start_nodes = [
    # {'host':'127.0.0.1', 'port':'8866'},
    {'host':'127.0.0.1', 'port':'8865'}
]
src = StrictRedisCluster(startup_nodes=start_nodes,
                         decode_responses=True)
print(src.set('123','hello'))
print(src.set('test2', 'world'))
