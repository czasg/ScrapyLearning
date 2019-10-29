from pywss import Pyws, route, RadioMiddleware, PublicConfig, logging

try:
    from database import get_today_count
except:
    raise Exception('没有数据库配置文件，无法运行哦')

PublicConfig.RADIO_TIME = 10


class Radio(RadioMiddleware):
    @classmethod
    def process_data(cls):
        count = get_today_count()
        return '{}'.format(count)


@route('/ws/api/news/data')
def api_news_data(request, data):
    """ There's nothing to do """


if __name__ == '__main__':
    ws = Pyws(__name__, address='0.0.0.0', port=8868)
    ws.add_middleware(Radio)
    ws.serve_forever()
