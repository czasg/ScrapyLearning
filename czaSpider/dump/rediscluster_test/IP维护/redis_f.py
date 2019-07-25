import redis


db = redis.StrictRedis(host='127.0.0.1', port=6379)
# db.set('cza:test', 'hello cza')
# print(db.get('cza:test'))

print(db.zscore('czatest', 'test1'))
# db.zadd('czatest', test1=10)
