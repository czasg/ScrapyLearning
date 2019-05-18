from czaSpider.czaTools import cover_dict

from .mongo_database import default_config as default_mongo
from .mongo_database import cover_default as cover_mongo

MONGO_INFO = cover_dict(default_mongo.MONGO_INFO, cover_mongo.MONGO_INFO)

from .mysql_database import default_config as default_mysql
from .mysql_database import cover_default as cover_mysql

MYSQL_INFO = cover_dict(default_mysql.MYSQL_INFO, cover_mysql.MYSQL_INFO)

from .redis_database import default_config as default_redis
from .redis_database import cover_default as cover_redis

REDIS_INFO = cover_dict(default_redis.REDIS_INFO, cover_redis.REDIS_INFO)

FID_SERVER = "http://127.0.0.1:9000/"
