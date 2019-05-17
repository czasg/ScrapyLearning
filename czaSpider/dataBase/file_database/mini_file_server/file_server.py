import logging

from aiohttp import web

routers = web.RouteTableDef()


@routers.post('/file')
def file_store(request):
    pass


app = web.Application()
app.add_routes(routers)
logging.info('http://127.0.0.1:9000 server start...')
web.run_app(app, host='127.0.0.1', port=9000)
