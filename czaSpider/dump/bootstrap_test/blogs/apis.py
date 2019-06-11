from tools import *


@get('/')
async def index():
    return {'__template__': 'index.html'}
