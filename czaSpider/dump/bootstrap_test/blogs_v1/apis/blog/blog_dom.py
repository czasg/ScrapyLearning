from handler import get
from models import Blog, Comment, SonComment
from tools.public_func import text2html
from tools.man_error import APIResourceError
from tools.safe_check_user import check_admin
from tools.man_pager import get_page_index


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
        'api': '/api/edit/blog/%s' % id  # todo, 为啥要加这个呢，在里面直接定义好不就行了吗，只要接口不改变的话，这种接口肯定是写在前段啊
    }


@get('/blogs/blog/{id}')  # todo, 内容要和评论拆开,博客内容要以接口的形式返回，而不是直接返回一个大文档
async def detail_blog(id):
    return {
        '__template__': 'blog_detail.html',
        'id': id,
        'api': '/api/edit/blog/%s' % id
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
