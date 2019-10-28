import jieba
import time
import re
import json

from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict
from concurrent import futures

executor = futures.ThreadPoolExecutor(3)

area = {
    '11': '北京',
    '12': '天津',
    '13': '河北',
    '14': '山西',
    '15': '内蒙古',
    '21': '辽宁',
    '22': '吉林',
    '23': '黑龙江',
    '31': '上海',
    '32': '江苏',
    '33': '浙江',
    '34': '安徽',
    '35': '福建',
    '36': '江西',
    '37': '山东',
    '41': '河南',
    '42': '湖北',
    '43': '湖南',
    '44': '广东',
    '45': '广西',
    '46': '海南',
    '50': '重庆',
    '51': '四川',
    '52': '贵州',
    '53': '云南',
    '54': '西藏',
    '61': '陕西',
    '62': '甘肃',
    '63': '青海',
    '64': '宁夏',
    '65': '新疆',
    '71': '台湾',
    '81': '香港',
    '82': '澳门',
}


def choose_province(city_code):
    try:
        return area[city_code]
    except:
        raise Exception('异常省份编码: {}'.format(city_code))


def get_now_datetime():
    return datetime.now()


def get_today_datetime(now):
    return datetime(now.year, now.month, now.day)


def get_yesterday_datetime(today):
    return today - timedelta(days=1)


def get_tomorrow_datetime(today):
    return today + timedelta(days=1)


class Mongodb:
    def __init__(self, online=False):
        self._client = None
        self.online = online
        self.connect_mongodb()

    @property
    def client(self):
        assert self._client, 'Mongodb Client Cannot Be None!'
        return self._client

    def connect_mongodb(self):
        if self.online:
            online_paras = {
                "host": ["192.168.0.31", "192.168.0.32", "192.168.0.33", ],
                "port": 23333,
                "replicaSet": "data_online",
                "readPreference": "secondaryPreferred",

                "username": "taohui",
                "password": "zhengwubaike",
            }
        else:
            online_paras = {
                "host": "192.168.0.91",
                "port": 27017,
                "readPreference": "secondaryPreferred",
            }
        self._client = MongoClient(**online_paras)


mongodb = Mongodb(online=True)
mongodb_offline = Mongodb(online=False)
RE_SEARCH_PROVINCE = re.compile('.*?(\d{2})').search
RE_SEARCH_DAY = re.compile('(.*?)\s').search


def get_collection_statistical(db='新闻(新闻)',
                               filter_db='',
                               filter_keys=None,
                               timestamp_day=None,
                               pprint=True,
                               save=True,
                               filter_db_end=''):
    timestamp_yesterday = timestamp_day - timedelta(days=1)
    timestamp_tomorrow = timestamp_day + timedelta(days=1)
    result = defaultdict(dict)
    db_handler = mongodb.client[db]
    collections = db_handler.list_collection_names()
    all_jieba_list = []
    for collection in collections:
        try:
            if collection.startswith(filter_db) and collection.endswith(filter_db_end):
                if pprint:
                    print('当前正在处理：{}'.format(collection))
                jieba_list = []
                count = 0
                for doc in db_handler[collection].find(
                        {'$and': [{'发布日期': {'$gt': timestamp_day}}, {'发布日期': {'$lt': timestamp_tomorrow}}]},
                        dict(zip(filter_keys, [1 for _ in range(len(filter_keys))]), _id=0)
                        if filter_keys else None):
                    jieba_list.extend(jieba.lcut(doc[filter_keys[0]])) if filter_keys else None
                    all_jieba_list.extend(jieba_list) if not save and jieba_list else None
                    count += 1
                result[collection]['count'] = count
                result[collection]['timestamp'] = int(timestamp_day.timestamp())
                result[collection]['province'] = choose_province(RE_SEARCH_PROVINCE(collection).group(1))
                if save:
                    abnormal = 0 if result[collection]['count'] else \
                        (mongodb_offline.client[db + '-offline-cza'][collection].
                         find_one({'timestamp': int(timestamp_yesterday.timestamp())}) or {}).get('abnormal', 0) + 1
                    mongodb_offline.client[db + '-offline-cza'][collection].update_one(
                        {'timestamp': result[collection]['timestamp']},
                        {'$set': dict(**result[collection], jieba_list=json.dumps(jieba_list, ensure_ascii=False),
                                      abnormal=abnormal)},
                        upsert=True)
        except Exception as e:
            print(e)
            continue
    mongodb.client.close()
    mongodb_offline.client.close()
    return result, all_jieba_list


if __name__ == '__main__':
    start = time.time()

    today = get_today_datetime(get_now_datetime())
    y = get_yesterday_datetime(today)
    yy = get_yesterday_datetime(y)
    yyy = get_yesterday_datetime(yy)
    t = get_tomorrow_datetime(today)

    get_collection_statistical(db='新闻(新闻)', filter_db='人民政府', filter_keys=['标题'], timestamp_day=today)

    print(time.time() - start)
