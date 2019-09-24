import time, re

from database.redis.database_redis import redis_handler, REDIS_USER_SNOW_ID
from web_socket.socket_error import AuthenticationError


class TokenChecker:

    @classmethod
    def check(cls, info):
        try:
            if 'czaOrz=' in info:
                info = re.search('czaOrz=(.*?)(?=;|$)', info).group(1)
            uid, expires, sha1 = info.split('-')
            if redis_handler.hexists(REDIS_USER_SNOW_ID, uid) and float(expires) > time.time():
                return uid
        except:
            pass
        return AuthenticationError
