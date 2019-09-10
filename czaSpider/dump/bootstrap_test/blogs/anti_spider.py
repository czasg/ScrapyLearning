from tools import *
from aiohttp import web
ANTI_COOKIE_FIRST = 'anti_spider_first'
async def anti_spider_first(app, handler):
    async def _anti_spider_first(request):
        anti_cookie = request.cookies.get(ANTI_COOKIE_FIRST)
        print(anti_cookie)
        if not request.path.startswith('/get/init/anti/cookie'):
            if anti_cookie:
                anti = check_anti_spider(anti_cookie)
                if anti == None:
                    return web.HTTPFound('/get/init/anti/cookie')
                elif anti == 'True':
                    pass  # todo, add anti spider
            else:
                return web.HTTPFound('/get/init/anti/cookie')
        return (await handler(request))

    return _anti_spider_first


async def anti_spider_second(app, handler):
    async def _anti_spider_second(request):
        anti_cookie = request.cookies.get(ANTI_COOKIE)
        if not request.path.startswith('/get/init/anti/cookie'):
            if anti_cookie:
                anti = check_anti_spider(anti_cookie)
                if anti == None:
                    return web.HTTPFound('/get/init/anti/cookie')
                elif anti == 'True':
                    pass  # todo, add anti spider
            else:
                return web.HTTPFound('/get/init/anti/cookie')
        return (await handler(request))

    return _anti_spider_second