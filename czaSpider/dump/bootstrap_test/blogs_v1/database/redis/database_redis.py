from redis import StrictRedis


class Redis:
    client = None

    @classmethod
    def get_redis_client(cls):
        if not cls.client:
            cls.client = StrictRedis()
        return cls.client


REDIS_ANTI_SPIDER_TIME = 'anti_spider_time'
COUNT_EXPIRE_TIME = 60  # 24 * 60 * 60
COUNT_FORBID_TIME = 20
redis_handler = Redis.get_redis_client()
