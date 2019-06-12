from handler import get

@get('/')
async def index():
    return {'__template__': 'index.html'}
