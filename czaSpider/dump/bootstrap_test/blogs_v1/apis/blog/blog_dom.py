from tools.handler import get
from tools.man_error import APIResourceError
from tools.safe_check_user import check_admin
from tools.man_pager import get_page_index
from tools.public_func import *
from database.mysql.models import *


@get('/blog/blogs')
async def blogs(): return {'__template__': 'blog/blogs.html'}


@get('/blog/manage')
async def manage_blogs(request, *, page='1'):
    if request.__user__ is None:
        raise APIResourceError('请先登陆', 'No Login')
    return {
        '__template__': 'manage/manage_blog.html',
        'page_index': get_page_index(page)
    }


@get('/blog/new')
def new_blog():
    return {
        '__template__': 'blog/blog_editor.html',
        'id': '',
        'api': '/api/new/blog'
    }


@get('/blog/edit/{id}')
def edit_blog(*, id):
    return {
        '__template__': 'blog/blog_editor.html',
        'id': id,
        'api': '/api/edit/blog/%s' % id
    }


@get('/blog/detail/{id}')
async def detail_blog(id):
    blog = await Blog.find(int(id))
    blog.count += 1
    await blog.update_table()
    comments = await Comment.findAll('blog_id=?', [int(id)], orderBy='created_at desc')
    for c in comments:
        c.html_content = text2html(c.content)
        c['id'] = str(c['id'])
        sons = await SonComment.findAll('comment_id=?', [int(c.id)], orderBy='created_at')
        for s in sons:
            s.html_content = text2html(s.content)
            s['id'] = str(s['id'])
        c.son_comments = sons
        c.son_comments_nums = len(sons)
    blog.html_content = blog.content
    return {
        '__template__': 'blog/blog_detail.html',
        'blog': blog,
        'comments': comments
    }


"""
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
"""
