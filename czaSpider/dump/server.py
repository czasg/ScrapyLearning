import logging
import aiohttp
import asyncio

from aiohttp import web

logging.basicConfig(level=logging.INFO)

routers = web.RouteTableDef()


@routers.post('/')
async def file_store(request):
    reader = await request.multipart()
    file = await reader.next()
    fileName = file.filename if file.filename else "NoName"
    size = 0
    with open('testNew', 'wb') as f:
        while True:
            chunk = await file.read_chunk(size=1024)
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)

    return web.json_response(data={"res":"done"})

app = web.Application()
app.add_routes(routers)
logging.info('http://127.0.0.1:9000 server start...')
web.run_app(app, host='127.0.0.1', port=9000)

