import time

from tools.handler import get, post
from database.mysql.models import Blog, Comment
from tools.man_error import APIResourceError
from tools.man_pager import *
from tools.sim_engine import *
from tools.public_func import save_image
from tools.idgen import id_pool


@get('/api/get/blogs')
async def api_get_blogs(request, *, page='1', page_size=None, user_id=None):
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)')
    p = Pager(num, page_index, get_page_size(page_size)) if page_size else Pager(num, page_index)
    if num == 0:
        return dict(page=0, blogs=())
    if request.__user__ and request.__user__.admin:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    elif user_id:
        blogs = await Blog.findAll('user_id=?', [user_id], orderBy='created_at desc', limit=(p.offset, p.limit))
    else:
        blogs = await Blog.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for b in blogs:
        b['id'] = str(b['id'])
        b['user_id'] = str(b['user_id'])
    return dict(page=p, blogs=blogs)

@get('/api/get/all/blog/type')
async def api_get_all_blog_type():
    blogs = await Blog.findAll(orderBy='created_at desc')
    res = {}
    for blog in blogs:
        res[str(blog.blog_type)] = res.get(str(blog.blog_type), 0) + 1
    return res


@get('/api/get/blog/{id}')
async def api_get_blog(*, id): return (await Blog.find(int(id)))


@post('/api/new/blog')
async def api_new_blog(request, *, title, summary, content, blog_image, blog_type):
    if not title or not title.strip():
        raise APIResourceError('文章标题不能为空', 'None Title For Blog')
    if not summary or not summary.strip():
        raise APIResourceError('文章摘要不能为空', 'None Summery For Blog')
    if not content or not content.strip():
        raise APIResourceError('文章内容不能为空', 'None Text For Blog')
    blog_id = id_pool.next_id()
    if blog_image and blog_image.startswith('data:image'):
        blog_image = save_image(blog_id, re.search('.*?base64,(.*)', blog_image).group(1))
    blog = Blog(id=blog_id, user_id=request.__user__.id, user_name=request.__user__.name,
                user_image=request.__user__.image, blog_image=blog_image, blog_type=blog_type,
                title=title.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    blog['id'] = str(blog['id'])
    return blog


@post('/api/edit/blog/{id}')
async def api_edit_blog(id, *, title, summary, content, blog_image, blog_type):
    if not title or not title.strip():
        raise APIResourceError('文章标题不能为空', 'None Title For Blog')
    if not summary or not summary.strip():
        raise APIResourceError('文章摘要不能为空', 'None Summery For Blog')
    if not content or not content.strip():
        raise APIResourceError('文章内容不能为空', 'None Text For Blog')
    blog = await Blog.find(int(id))
    blog.title = title.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    blog.blog_type = int(blog_type)
    if blog_image and blog_image.startswith('data:image/png;base64,'):
        blog.blog_image = save_image(blog.id, blog_image[22:])
    blog.update_at = time.time()
    await blog.update_table()
    blog['id'] = str(blog['id'])
    return blog


@post('/api/drop/blog/{id}')  # todo, 评论和文章一起删除吗，还是发起两次算了
async def api_drop_blog(request, *, id):
    blog = await Blog.find(int(id))
    if request.__user__.admin or blog.user_id == request.__user__.id:
        comments = await Comment.findAll('blog_id=?', str(blog.id))
        for comment in comments:
            await comment.remove()
        await blog.remove()
        return dict(id=str(id))
    raise APIResourceError('无发执行此类操作', 'Not Admin')


@post('/api/find/blog/by/engine')
async def api_find_blog_by_engine(*, user_input):
    result = SimEngine.search(user_input)
    if not result:
        return dict(error='未查询到相关补给资源~')
    results = re.sub('\[(.*)\]', '(\\1)', str(result))
    blogs = await Blog.findAll(where='id in %s' % results, orderBy='created_at desc', limit=(0, 10))
    return dict(blogs=blogs)

# todo This is just Test-API-Data
@get('/api/get/blogs/statistic')
async def api_get_blogs_statistic():
    return {
        'dataSet': [{'data':[1,2,3]}],
        'timeline': {'data': [201901,201902,201903]}
    }
@get('/api/get/multi/statistic')
async def api_get_multi_statistic():
    return {
        'dataSet': [{'name': 'test', 'data': [1,2,3]}],
        'timeline': {'data': [201901,201902,201903]}
    }
@get('/api/get/multi/statistic/github_info')
async def api_get_multi_statistic_github_info(*, start_year=2019):
    return {
        'dataSet': [{'data':[1,2,3]}],
        'timeline': {'data': [201901,201902,201903]}
    }