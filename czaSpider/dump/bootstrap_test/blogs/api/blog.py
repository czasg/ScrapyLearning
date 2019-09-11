from tools.handler import get, post
from simengine import SimEngine

logger = logging.getLogger(__name__)


@get('/')
async def index(): return {'__template__': 'index.html'}


@get('/blogs')
async def blogs(): return {'__template__': 'blogs.html'}


@get('/root/manage/blogs')
async def root_manage_blogs(request, *, page='1'):
    check_admin(request)
    return {
        '__template__': 'root_manage_blogs.html',
        'page_index': get_page_index(page)
    }


@get('/manage/blogs')
async def manage_blogs(request, *, page='1'):
    if request.__user__ is None:
        raise APIResourceError('请先登陆', 'No Login')
    return {
        '__template__': 'manage_blogs.html',
        'page_index': get_page_index(page)
    }


@get('/new/blog')
def new_blog():
    return {
        '__template__': 'blog_editor.html',
        'id': '',
        'api': '/api/new/blog'
    }


@get('/edit/blog/{id}')
def edit_blog(*, id):
    return {
        '__template__': 'blog_editor.html',
        'id': id,
        'api': '/api/edit/blog/%s' % id
    }


@get('/blogs/blog/{id}')
async def detail_blog(id):
    blog = await Blog.find(id)
    blog.count += 1
    await blog.update_table()
    comments = await Comment.findAll('blog_id=?', [id], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
        sons = await SonComment.findAll('comment_id=?', [c.id], orderBy='created_at')
        for s in sons:
            s.html_content = text2html(s.content)
        c.son_comments = sons
        c.son_comments_nums = len(sons)
    blog.html_content = blog.content
    return {
        '__template__': 'blog_detail.html',
        'blog': blog,
        'comments': comments
    }


@get('/api/get/blogs')
async def api_get_blogs(*, page='1', page_size=None, user_id=None):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Pager(num, page_index, get_page_size(page_size)) if page_size else Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    if user_id:
        blogs = await Blog.findAll('user_id=?', [user_id], orderBy='created_at desc', limit=(p.offset, p.limit))
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/api/get/blog/{id}')
async def api_get_blog(*, id): return (await Blog.find(id))


@post('/api/new/blog')
async def api_new_blog(request, *, name, summary, content):
    if not name or not name.strip():
        raise APIResourceError('文章标题不能为空', 'None Title For Blog')
    if not summary or not summary.strip():
        raise APIResourceError('文章摘要不能为空', 'None Summery For Blog')
    if not content or not content.strip():
        raise APIResourceError('文章内容不能为空', 'None Text For Blog')
    blog = Blog(user_id=request.__user__.id, user_name=request.__user__.name, user_image=request.__user__.image,
                name=name.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@post('/api/edit/blog/{id}')
async def api_edit_blog(id, *, name, summary, content):
    blog = await Blog.find(id)
    if not name or not name.strip():
        raise APIResourceError('文章标题不能为空', 'None Title For Blog')
    if not summary or not summary.strip():
        raise APIResourceError('文章摘要不能为空', 'None Summery For Blog')
    if not content or not content.strip():
        raise APIResourceError('文章内容不能为空', 'None Text For Blog')
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    blog.update_at = time.time()
    await blog.update_table()
    return blog


@post('/api/drop/blog/{id}')
async def api_drop_blog(*, id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', blog.id)
    for comment in comments:
        await comment.remove()
    await blog.remove()
    return dict(id=id)


@post('/api/find/blog/by/engine')
async def api_find_blog_by_engine(*, user_input):
    result = SimEngine.search(user_input)
    if not result:
        return dict(error='未查询到相关补给资源~')
    results = re.sub('\[(.*)\]', '(\\1)', str(result))
    blogs = await Blog.findAll(where='id in %s' % results, orderBy='created_at desc', limit=(0, 10))
    return dict(blogs=blogs)
