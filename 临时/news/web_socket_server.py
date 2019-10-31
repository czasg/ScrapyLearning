from pywss import Pyws, route, RadioMiddleware, PublicConfig, json, ConnectManager


@route('/ws/api/news/data')
def api_news_data(request, data):
    json_data = json.loads(data)
    if json_data.get('start') == True:
        request.conn.send_to_all({'online': ConnectManager.online()})
        return {'name': request.conn.name}
    msg = json_data.get('msg')
    if msg:
        request.conn.send_to_all({'from': request.conn.name, 'msg': msg})


if __name__ == '__main__':
    ws = Pyws(__name__, address='0.0.0.0', port=8868)
    # ws.add_middleware(Radio)
    ws.serve_forever()

# try:
#     from database import get_today_count
# except:
#     raise Exception('没有数据库配置文件，无法运行哦')
# PublicConfig.RADIO_TIME = 10
# class Radio(RadioMiddleware):
#     @classmethod
#     def process_data(cls):
#         count = get_today_count()
#         return {'radio': 'radio', 'count': count}
