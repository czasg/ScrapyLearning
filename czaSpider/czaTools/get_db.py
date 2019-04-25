import os
import time
import pymongo
import sqlite3
import redis

from czaSpider.settings import MONGO_INFO,sqlite3_INFO,REDIS_INFO,shubo_mongo
from czaSpider.czaTools.path_func import get_current_path, to_path, get_database_path


def get_mongo_client():
    return pymongo.MongoClient(**MONGO_INFO)
    # return pymongo.MongoClient(**shubo_mongo)

def get_sqlite3_connection(timeStr=False):
    if timeStr:
        timeStr = time.strftime("%Y%m%d", time.localtime())
        dbName = timeStr + '_' +  sqlite3_INFO["host"]
        return sqlite3.connect(to_path(get_database_path(), dbName))
    conn = sqlite3.connect(to_path(get_database_path(), sqlite3_INFO["host"]))
    return conn

def execute_sql(conn, sql):
    conn.cursor().execute(sql)
    conn.commit()
    conn.cursor().close()
    conn.close()

def get_redis_client():
    pass

def open_mongodb():
    os.system(r"D:\mongoddbb\bin\mongod --dbpath {}".format(get_database_path()))
    os.system("net start MongoDB")

if __name__ == "__main__":
    # open_mongodb()
    # a = get_mongo_client()
    # import os
    # os.remove("sqlite3.db")

    # client = get_mongo_client()
    # coll = client["save-source"]["test"]
    # coll.insert_one({"test":"test"})

    conn = get_sqlite3_connection(timeStr=True)
    # sql = """create table source (author varchar(10), more varchar(200), releaseTime varchar(20), source varchar(200), spiderName varchar(100), url varchar(100))"""
    # sql = """drop table source"""
    sql = """select * from source"""
    conn.cursor().execute(sql)
    print(conn.cursor().fetchall())