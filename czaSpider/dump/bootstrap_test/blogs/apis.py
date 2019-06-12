from handler import get, post


@get('/')
async def index():
    return {'__template__': 'index.html'}


@get('/test')
async def login():
    print('login')
    return {'__template__': 'test.html'}
