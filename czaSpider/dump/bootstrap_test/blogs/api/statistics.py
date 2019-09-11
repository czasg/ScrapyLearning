from datetime import timedelta
# from motor.motor_asyncio import AsyncIOMotorClient
import pymongo

from tools.handler import get

logger = logging.getLogger(__name__)
# client = AsyncIOMotorClient()
client = pymongo.MongoClient('127.0.0.1', 27017)

@get('/api/get/blogs/statistic')
async def api_get_blogs_statistic(*, limit=7):
    _date = get_now_datetime()
    pre = None
    nums = []
    times = []
    for i in range(limit):
        count = await Blog.findNumber('count(id)', where='update_at > %s' % _date.timestamp())
        if i == 0:
            pre = count
            nums.append(count)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
        else:
            nums.append(count - pre)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
            pre = count
        _date = _date - timedelta(days=1)
    return dict(nums=nums[::-1], times=times[::-1])


@get('/api/get/housePrice/statistic')
async def api_get_housePrice_statistic(*, dbName, collectionName, limit=7):
    _date = get_now_datetime()
    pre = None
    nums = []
    times = []
    db = client[dbName[0]]
    collection = db[collectionName[0]]
    for i in range(limit):
        query = process_commands(gte={"download_time": _date.timestamp()})
        count = await collection.count_documents(query)
        if i == 0:
            pre = count
            nums.append(count)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
        else:
            nums.append(count - pre)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
            pre = count
        _date = _date - timedelta(days=1)
    return dict(nums=nums[::-1], times=times[::-1])


@get('/api/get/multi/statistic')
async def api_get_multi_statistic(*, dbNames_and_collectionNames, limit=7):
    _date = get_now_datetime()
    res = {}
    for di in dbNames_and_collectionNames[0]:
        pre = None
        nums = []
        times = []
        for dbName, collectionName in di.items():
            collection = client[dbName][collectionName]
            for i in range(limit):
                query = process_commands(gte={"download_time": _date.timestamp()})
                count = await collection.count_documents(query)
                if i == 0:
                    pre = count
                    nums.append(count)
                    times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
                else:
                    nums.append(count - pre)
                    times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
                    pre = count
                _date = _date - timedelta(days=1)
            res.setdefault(collectionName, dict(nums=nums[::-1], times=times[::-1]))
    return res
