from redis import StrictRedis


class Redis:
    client = None

    @classmethod
    def get_redis_client(cls):
        if not cls.client:
            cls.client = StrictRedis()
        return cls.client


REDIS_ANTI_SPIDER_TIME = 'anti_spider_time'
COUNT_EXPIRE_TIME = 24 * 60 * 60
COUNT_CAPTCHA_TIME = 2000000
COUNT_FORBID_TIME = 3000000
CAPTCHA_EXPIRE_TIME = 15
redis_handler = Redis.get_redis_client()

if __name__ == '__main__':
    redis_handler.set('127.0.0.1', 1, COUNT_EXPIRE_TIME)
