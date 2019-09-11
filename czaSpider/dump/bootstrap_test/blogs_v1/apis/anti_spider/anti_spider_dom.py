from tools.handler import get


@get('/get/anti/spider/first')
def get_anti_spider_first():
    return {'__template__': 'anti_spider/anti_spider_first.html'}


@get('/get/anti/spider/second')
def get_anti_spider_second(request):
    return {'__template__': 'anti_spider/anti_spider_second.html'}
