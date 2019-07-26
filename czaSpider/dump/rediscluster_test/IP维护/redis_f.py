import redis

db = redis.StrictRedis(host='127.0.0.1', port=6379)

test = db.pipeline()

# db.set('cza:test', 'hello cza')
# print(db.get('cza:test'))

# print(db.zscore('proxy_ip', '47.101.42.79:8000'))
print(db.zrangebyscore('proxy_ip', 0, 100))
# db.zadd('czatest', test1=10)
