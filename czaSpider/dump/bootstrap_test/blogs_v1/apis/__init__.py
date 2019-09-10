from .blog.blog_api import *
from .blog.blog_dom import *

from handler import get


@get('/')
async def index(): return {'__template__': 'index.html'}
