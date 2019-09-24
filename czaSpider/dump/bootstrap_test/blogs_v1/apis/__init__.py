from .blog.blog_api import *
from .blog.blog_dom import *
from .user.user_api import *
from .user.user_dom import *
from .comment.comment_api import *

from tools.handler import get


@get('/')
async def index(): return {'__template__': 'index.html'}
