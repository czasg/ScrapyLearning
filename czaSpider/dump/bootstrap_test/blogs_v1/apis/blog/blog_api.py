import time

from handler import get, post
from models import Blog, Comment
from tools.man_error import APIResourceError
from tools.man_pager import *
from tools.sim_engine import *
from tools.public_func import save_image
from tools.idgen import id_pool


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


@post('/api/new/blog')  # todo, 创建新blog的时候，需要加入图片，此时的图片应该是二进制的形式，保存图片，存图片的路径即可
async def api_new_blog(request, *, title, summary, content, image):
    if not title or not title.strip():
        raise APIResourceError('文章标题不能为空', 'None Title For Blog')
    if not summary or not summary.strip():
        raise APIResourceError('文章摘要不能为空', 'None Summery For Blog')
    if not content or not content.strip():
        raise APIResourceError('文章内容不能为空', 'None Text For Blog')
    blog_id = id_pool.next_id()
    blog_image = save_image(blog_id, image)
    blog = Blog(id=blog_id, user_id=request.__user__.id, user_name=request.__user__.name,
                user_image=request.__user__.image, blog_image=blog_image,
                title=title.strip(), summary=summary.strip(), content=content.strip())
    await blog.save()
    return blog


@post('/api/edit/blog/{id}')  # todo, 更新图片如何执行，前段设计的是如何传递的呢，这个到时可以看看
async def api_edit_blog(id, *, name, summary, content, image=None):
    if not name or not name.strip():
        raise APIResourceError('文章标题不能为空', 'None Title For Blog')
    if not summary or not summary.strip():
        raise APIResourceError('文章摘要不能为空', 'None Summery For Blog')
    if not content or not content.strip():
        raise APIResourceError('文章内容不能为空', 'None Text For Blog')
    blog = await Blog.find(id)
    blog.name = name.strip()
    blog.summary = summary.strip()
    blog.content = content.strip()
    blog.update_at = time.time()
    await blog.update_table()
    return blog


@post('/api/drop/blog/{id}')  # todo, 评论和文章一起删除吗，还是发起两次算了
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
