import json
from pyws import Pyws
from pyws.route import route
"""
每个开发人员应可以创建自己的数据字段
那么我就又需要类似一种field的机制咯，这玩意该怎么写呀
"""# todo

@route('/new')
def new(request, data):
    print(type(data), data)
    return data


@route('/test')
def test(request, data):
    print(type(data), data)
    return 'hello world'


if __name__ == '__main__':
    test = Pyws(__name__)
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
