import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("s1.html")

    def post(self, *args, **kwargs):
        pass


users = set()


class ChatHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args, **kwargs):
        '''客户端连接'''
        print("connect....")
        print(self.request)
        users.add(self)

    def on_message(self, message):
        '''有消息到达'''
        now = datetime.datetime.now()
        content = self.render_string("recv_msg.html", date=now.strftime("%Y-%m-%d %H:%M:%S"), msg=message)
        for client in users:
            if client == self:
                continue
            client.write_message(content)

    def on_close(self):
        '''客户端主动关闭连接'''
        users.remove(self)


st = {
    "template_path": "template",  # 模板路径配置
    "static_path": 'static',
}

# 路由映射   匹配执行，否则404
application = tornado.web.Application([
    ("/index", MainHandler),
    ("/wschat", ChatHandler),
], **st)

if __name__ == "__main__":
    application.listen(8080)

    # io多路复用
    tornado.ioloop.IOLoop.instance().start()
