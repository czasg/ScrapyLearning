from datetime import timedelta
from motor.motor_asyncio import AsyncIOMotorClient

from handler import get, post
from tools import *

logger = logging.getLogger(__name__)
client = AsyncIOMotorClient('127.0.0.1', 27017)


@get('/api/get/blogs/statistic')
async def api_get_blogs_statistic(*, limit=7):
    _date = get_now_datetime()
    pre = None
    # statistics = {}
    nums = []
    times = []
    for i in range(limit):
        count = await Blog.findNumber('count(id)', where='update_at > %s' % _date.timestamp())
        if i == 0:
            pre = count
            # statistics.setdefault('%s.%s.%s' % (_date.year, _date.month, _date.day), count)
            nums.append(count)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
        else:
            # statistics.setdefault('%s.%s.%s' % (_date.year, _date.month, _date.day), count - pre)
            nums.append(count - pre)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
            pre = count
        _date = _date - timedelta(days=1)
    # return statistics
    # nums.reverse()
    # times.reverse()
    # return dict(nums=nums, times=times)
    return dict(nums=nums[::-1], times=times[::-1])


@get('/api/get/housePrice/statistic')
async def api_get_housePrice_statistic(*, dbName, collectionName, limit=7):
    _date = get_now_datetime()
    pre = None
    # statistics = {}
    nums = []
    times = []
    db = client[dbName[0]]
    collection = db[collectionName[0]]
    for i in range(limit):
        query = process_commands(gte={"download_time": _date.timestamp()})
        count = await collection.count_documents(query)
        if i == 0:
            pre = count
            # statistics.setdefault('%s.%s.%s' % (_date.year, _date.month, _date.day), count)
            nums.append(count)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
        else:
            # statistics.setdefault('%s.%s.%s' % (_date.year, _date.month, _date.day), count - pre)
            nums.append(count - pre)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
            pre = count
        _date = _date - timedelta(days=1)
    # return statistics
    # nums.reverse()
    # times.reverse()
    # return dict(nums=nums, times=times)
    return dict(nums=nums[::-1], times=times[::-1])
