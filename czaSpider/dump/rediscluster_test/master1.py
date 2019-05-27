import redis

a = redis.StrictRedis(port=8866)

a.set('aaa','bbb')
print(a.get('aaa'))