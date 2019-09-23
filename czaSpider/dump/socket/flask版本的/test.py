from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template, request
import pickle

app = Flask(__name__)
app.secret_key = 'xfsdfqw'


@app.route('/index')
def index():
    return render_template('index.html')


WS_LIST = []


@app.route('/test')
def test():
    ws = request.environ.get('wsgi.websocket')
    if not ws:
        return '请使用WebSocket协议'
    # websocket连接已经成功
    WS_LIST.append(ws)
    while True:
        # 等待用户发送消息，并接受
        message = ws.receive()
        print(message)

        # 关闭：message=None
        if not message:
            print("ws.close")
            WS_LIST.remove(ws)
            ws.close()
            break

        for item in WS_LIST:
            item.send(message)

    return "asdfasdf"


if __name__ == '__main__':
    http_server = WSGIServer(('127.0.0.1', 5000,), app, handler_class=WebSocketHandler)
    http_server.serve_forever()