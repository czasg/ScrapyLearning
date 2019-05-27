from czaSpider.dataBase.redis_database.orm import get_redis_client, BaseRedis


if __name__ == '__main__':
    if get_redis_client():
        cza = BaseRedis('test', 'hello')
        # print(cza.push('test3', 'test4').memNum)
        # print(cza.memCount, cza.memNum)
        # print(cza.pop().doc)
        print(cza.exist())
        # cza.close()