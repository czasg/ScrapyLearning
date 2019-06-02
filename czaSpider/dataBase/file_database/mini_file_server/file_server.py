import logging
import os
import time
import uuid

from aiohttp import web

from czaSpider.dataBase.file_database.mini_file_server.config import toPath

logger = logging.getLogger(__name__)
routers = web.RouteTableDef()


def next_id():
    return "%015d%s000" % (int(time.time() * 1000), uuid.uuid4().hex)


@routers.get('/fetch/{fileName}')
async def file_fetch(request):
    fileName = toPath(request.match_info["fileName"])
    if not os.path.exists(fileName):
        raise Exception()
    with open(fileName, 'rb') as f:
        content = f.read()
    return web.Response(body=content)


@routers.post('/upload/file')
async def file_store(request):
    reader = await request.multipart()
    file = await reader.next()
    fileName = next_id()
    size = 0
    with open(toPath(fileName), 'wb') as f:
        while True:
            chunk = await file.read_chunk(size=1024)
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)
    return web.json_response(data={"fid": fileName, "size": size})


app = web.Application()
app.add_routes(routers)
logger.info('http://127.0.0.1:9000 server start...')
web.run_app(app, host='127.0.0.1', port=9000)
