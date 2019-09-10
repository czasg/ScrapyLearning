import json
from handler import get, post
from tools import *

logger = logging.getLogger(__name__)
ANTI_COOKIE_FIRST = 'anti_spider_first'


@get('/anti_spider')
async def anti_spider_dom(request):
    print('???')
    return {'__template__': 'anti_spider/anti_spider.html'}


@get('/get/init/anti/cookie')
async def anti_spider_first(request):
    print('??')
    webResponse = web.HTTPFound('/anti_spider')
    webResponse.set_cookie(ANTI_COOKIE_FIRST, 'True', max_age=86400)
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps({'anti_spider_first': 'True'}, ensure_ascii=False).encode()
    return webResponse
