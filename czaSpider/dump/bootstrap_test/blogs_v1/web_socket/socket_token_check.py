import time

from database.redis.database_redis import redis_handler, REDIS_USER_SNOW_ID
from web_socket.socket_error import AuthenticationError


class TokenChecker:

    @classmethod
    def check(cls, info):
        try:
            uid, expires, sha1 = info.split('-')
            if float(expires) > time.time():
                user_name = redis_handler.get(REDIS_USER_SNOW_ID, uid)
                if user_name:
                    return str(user_name, encoding='utf-8')
        except:
            pass
        return AuthenticationError
