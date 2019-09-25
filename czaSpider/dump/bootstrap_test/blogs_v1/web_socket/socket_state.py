from collections import defaultdict
from database.redis.database_redis import *

ERROR_COUNT = 2


class Connector:
    def __init__(self, snow_key, request, client_address):
        self.snow_key = snow_key
        self.request = request
        self.client_address = ':'.join([str(i) for i in client_address])
        self.user_name = redis_handler.hget(REDIS_USER_SNOW_ID, snow_key).decode()


class ConnectManager:
    connectors = defaultdict(dict)
    groups = defaultdict(dict)
    big_home = {'big_home': {}}

    @classmethod
    def online(cls):
        return len(cls.connectors)

    @classmethod
    def clear(cls, name, key):
        if key in cls.connectors[name]:
            cls.connectors[name].pop(key)
        if key in cls.big_home['big_home']:
            cls.big_home['big_home'].pop(key)

    @classmethod
    def add_connector(cls, name, key, value):
        cls.connectors[name][key] = value

    @classmethod
    def add_group(cls, name, key, value):
        cls.groups[name][key] = value

    @classmethod
    def add_big_home(cls, key, value):
        cls.big_home['big_home'][key] = value

    @classmethod
    def group_exist(cls, key):
        return key in cls.groups

    @classmethod
    def group_exist_key(cls, name, key):
        return key in cls.groups[name]


if __name__ == '__main__':
    print(redis_handler.hgetall(REDIS_USER_SNOW_ID))
