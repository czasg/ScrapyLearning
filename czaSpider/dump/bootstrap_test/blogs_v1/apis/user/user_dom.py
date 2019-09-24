from tools.handler import get, web
from tools.safe_check_user import check_admin, COOKIE_NAME
from tools.man_pager import get_page_index


@get('/register')
async def register():
    return {
        '__template__': 'user/register.html',
        'register_url': '/api/new/user'
    }


@get('/register/root')
async def root_register():
    return {
        '__template__': 'user/register.html',
        'register_url': '/api/new/root/user'
    }


@get('/root/manage/users')
async def root_manage_users(request, *, page='1'):
    check_admin(request)
    return {
        '__template__': 'manage/manage_user.html',
        'page_index': get_page_index(page)
    }


@get('/signout')
def signout():
    webResponse = web.HTTPFound('/')
    webResponse.set_cookie(COOKIE_NAME, '-deleted-', max_age=0)
    return webResponse
