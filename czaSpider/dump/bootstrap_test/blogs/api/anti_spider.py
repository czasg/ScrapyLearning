import json
from tools.handler import get
from tools.handler import web

logger = logging.getLogger(__name__)
ANTI_COOKIE_FIRST = 'anti_spider_first'


@get('/anti_spider')
async def anti_spider_dom(request):
    return {'__template__': 'anti_spider/anti_spider.html'}


@get('/get/anti/cookie/first')
async def anti_spider_first(request):
    web.HTTPRedirection()
    webResponse = web.HTTPFound('/anti_spider')
    webResponse.set_cookie(ANTI_COOKIE_FIRST, 'True', max_age=86400)
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps({'anti_spider_first': 'True'}, ensure_ascii=False).encode()
    return webResponse

@get('/get/anti/cookie/second')
async def anti_spider_second(request):
    return {'__template__': 'anti_spider/anti_spider.html'}

