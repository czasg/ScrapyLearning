from pyws import Pyws
from pyws.route import route
from pyws.public import AuthenticationError
from pyws.middlewares import DaemonMiddleware, RadioMiddleware
import json
"""
每个开发人员应可以创建自己的数据字段
那么我就又需要类似一种field的机制咯，这玩意该怎么写呀
"""# todo

@route('/test')
def test(request, data):
    print(type(data), data)
    return 'hello world'

class CookieMiddleware(DaemonMiddleware):

    def process_input(self, request, input_msg):
        json_data = json.loads(input_msg)
        if 'name' not in json_data:
            raise AuthenticationError
        return str(json_data['name'])
class Radio(RadioMiddleware):
    def process_data(cls):
        return None
@route('/test2')
def test2(request, data):
    import json
    print(json.loads(data))  # todo, Cookie验证也是ok，那么就是可以多点进行接触的，怎么实现他们之间的交互呢，这是一个问题

if __name__ == '__main__':
    test = Pyws(__name__)
    # test.add_middleware([CookieMiddleware, Radio])
    test.serve_forever()

"""
ws =new WebSocket("ws://127.0.0.1:8866");
ws.onmessage = function (ev) {
    console.log(JSON.parse(ev.data));
}
ws.onclose = function (ev) {
    console.log('断开连接')
}
"""
