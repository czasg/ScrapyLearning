import time
import asyncio
import tornado.web
import tornado.ioloop


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world\n")


class NonBlocking(tornado.web.RequestHandler):
    async def get(self):
        await asyncio.sleep(10)


class Blocking(tornado.web.RequestHandler):
    def get(self):
        time.sleep(10)


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/non_blocking", NonBlocking),
        (r"/blocking", Blocking),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
