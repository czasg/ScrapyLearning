import json

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import timedelta

from tools.handler import get, post
from tools import _RE_EMAIL, _RE_SHA1
from simengine import SimEngine

client = AsyncIOMotorClient('127.0.0.1', 27017)
logger = logging.getLogger(__name__)


# 模板页面 #

@get('/')
async def index(): return {'__template__': 'index_show_data.html'}


@get('/register')  # '/api/new/user'
async def register(): return {'__template__': 'register.html', 'register_url': '/api/new/user'}


@get('/register/root')  # '/api/new/root/user'
async def root_register(): return {'__template__': 'register.html', 'register_url': '/api/new/root/user'}


@get('/blogs')
async def blogs():
    return {
        '__template__': 'show_blogs_all.html',
        'api_for_blog': '/api/get/blogs',
        'this_is_index_blogs': True
    }


@get('/blogs/{type}')
async def blogs_type(*, type):
    try:
        blog_type = int(type)
    except:
        raise APIResourceError('无相关资源', 'No Such Resource!')
    return {
        '__template__': 'show_blogs_all.html',
        'api_for_blog': '/api/get/blogs/%s' % blog_type,
        'this_is_index_blogs': True
    }


@get('/resume')
async def resume(): return {'__template__': 'resume.html'}


@get('/show/spider/data')
async def show_spider_data(): return {'__template__': 'show_spider_data.html'}


@get('/root/manage/users')
async def root_manage_users(request, *, page='1'):
    check_admin(request)
    return {
        '__template__': 'manage_users.html',
        'page_index': get_page_index(page)
    }


@get('/root/manage/blogs')
async def root_manage_blogs(request, *, page='1'):
    check_admin(request)
    return {
        '__template__': 'manage_blogs_root.html',
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
        '__template__': 'show_blog_editor.html',
        'id': '',
        'api': '/api/new/blog'
    }


@get('/edit/blog/{id}')
def edit_blog(*, id):
    return {
        '__template__': 'show_blog_editor.html',
        'id': id,
        'api': '/api/edit/blog/%s' % id
    }


@get('/color_choose')
def color_choose(): return {'__template__': '调色板.html'}


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
        '__template__': 'show_blog.html',
        'blog': blog,
        'comments': comments
    }


# 用户登陆认证、注册、退出、删除模块 #

@post('/api/authenticate')
async def authenticate(*, email, passwd):
    if not email or not passwd:
        raise APIResourceError('请输入有效的: 用户名/密码', 'apis-authenticate')
    user = await User.findAll('email=?', [email])
    if len(user) == 0:
        raise APIResourceError('用户名不存在', 'apis-authenticate')
    user = user[0]
    sha1 = hashlib.sha1()
    sha1.update(user.id.encode())
    sha1.update(b':')
    sha1.update(passwd.encode())
    if user.passwd != sha1.hexdigest():
        raise APIResourceError('密码错误', 'apis-authenticate')
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@post('/api/new/user')
async def api_register_user(*, name, email, passwd):
    if not name or not name.strip():
        raise APIResourceError('用户名不能为空', 'error Username')
    if not email or not _RE_EMAIL.match(email):
        raise APIResourceError('邮箱格式错误', 'error Email Format')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIResourceError('密码验证异常', 'Check SHA error')
    if email == 'root@ioco.com':
        raise APIResourceError('无法注册root用户', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='/static/img/user.png')  # % hashlib.md5(email.encode('utf-8')).hexdigest() todo, 增加用户头像
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@post('/api/new/root/user')
async def api_register_root_user(*, name, email, passwd):
    root = await User.findAll('email=?', ['root@ioco.com'])
    if len(root) > 0:
        raise APIResourceError('root用户已存在，请勿创建', 'root user has already existed!')
    if not name or not name.strip():
        raise APIResourceError('用户名不能为空', 'error Username')
    if email != 'root@ioco.com':
        raise APIResourceError('无法识别root邮箱', 'error Email Format')
    if not passwd or not _RE_SHA1.match(passwd):
        raise APIResourceError('密码验证异常', 'Check SHA error')
    user = await User.findAll('email=?', [email])
    if len(user) > 0:
        raise APIResourceDeplicated('邮件已被注册', 'Email has been alerdy registered!')
    uid = next_id()
    sha1_passwd = '%s:%s' % (uid, passwd)
    user = User(id=uid, name=name.strip(), email=email, admin=True,
                passwd=hashlib.sha1(sha1_passwd.encode()).hexdigest(),
                image='http://www.gravatar.com/avatar/%s?d=mm&s=120' % hashlib.md5(email.encode('utf-8')).hexdigest())
    await user.save()
    webResponse = web.Response()
    webResponse.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400)
    user.passwd = '******'
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps(user, ensure_ascii=False).encode()
    return webResponse


@get('/signout')
def signout():
    webResponse = web.HTTPFound('/')
    webResponse.set_cookie(COOKIE_NAME, '-deleted-', max_age=0)
    return webResponse


@post('/api/drop/user')
async def api_drop_user(request, *, id):
    check_admin(request)
    if request.__user__.id == id:
        raise APIResourceError('root用户无法删除，请联系管理员', 'root User can not be drop')
    user = await User.find(id)
    blogs = await Blog.findAll('user_id=?', [id])
    for blog in blogs:
        comments = await Comment.findAll('blog_id=?', blog.id)
        for comment in comments:
            await comment.remove()
        await blog.remove()
    await user.remove()
    return {'id': id}


# json请求接口 #

@get('/api/get/users')
async def api_get_users(*, page='1'):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    users = await User.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for u in users:
        u.passwd = '******'
    return dict(page=p, users=users)


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


@get('/api/get/blogs/{type}')
async def api_get_blogs_type(*, type, page='1', page_size=None, user_id=None):
    try:
        blog_type = int(type)
    except:
        raise APIResourceError('无相关资源', 'No Such Resource!')
    page_index = get_page_index(page)
    num = await Blog.findNumber('count(id)', where='blog_type=?', args=[blog_type])
    p = Pager(num, page_index, get_page_size(page_size)) if page_size else Pager(num, page_index)
    if num == 0:
        return dict(page=0, users=())
    if user_id:
        blogs = await Blog.findAll('user_id=?', [user_id], orderBy='created_at desc', limit=(p.offset, p.limit))
    else:
        blogs = await Blog.findAll(where='blog_type=?', args=[blog_type], orderBy='created_at desc',
                                   limit=(p.offset, p.limit))
    return dict(page=p, blogs=blogs)


@get('/api/get/blogs/statistic')
async def api_get_blogs_statistic(*, limit=7):
    _date = get_now_datetime()
    pre = None
    nums = []
    times = []
    for i in range(limit):
        count = await Blog.findNumber('count(id)', where='update_at > %s' % _date.timestamp())
        if i == 0:
            pre = count
            nums.append(count)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
        else:
            nums.append(count - pre)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
            pre = count
        _date = _date - timedelta(days=1)
    return dict(nums=nums[::-1], times=times[::-1])


@get('/api/get/housePrice/statistic')
async def api_get_housePrice_statistic(*, dbName, collectionName, limit=7):
    _date = get_now_datetime()
    pre = None
    nums = []
    times = []
    db = client[dbName[0]]
    collection = db[collectionName[0]]
    for i in range(limit):
        query = process_commands(gte={"download_time": _date.timestamp()})
        count = await collection.count_documents(query)
        if i == 0:
            pre = count
            nums.append(count)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
        else:
            nums.append(count - pre)
            times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
            pre = count
        _date = _date - timedelta(days=1)
    return dict(nums=nums[::-1], times=times[::-1])


@get('/api/get/blog/{id}')
async def api_get_blog(*, id): return (await Blog.find(id))


# 博客创建、删除模块 #

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


@post('/api/choose/blog/{id}/type')
async def api_choose_blog_type(id, request, *, current_type):
    user = request.__user__
    if user is None:
        raise APIResourceError('请先登陆', 'No User')
    blog = await Blog.find(id)
    try:
        blog_type = int(current_type)
    except:
        raise APIResourceError('error?', '??')
    blog.blog_type = blog_type
    await blog.update_table()
    return {}


@post('/api/drop/blog/{id}')
async def api_drop_blog(*, id):
    blog = await Blog.find(id)
    comments = await Comment.findAll('blog_id=?', blog.id)
    for comment in comments:
        await comment.remove()
    await blog.remove()
    return dict(id=id)


# 评论创建、删除、查询模块 #

@post('/api/new/comment/from/blog/{id}')
async def api_new_comment(id, request, *, content):
    user = request.__user__
    if user is None:
        raise APIResourceError('请先登陆', 'No User')
    if not content or not content.strip():
        raise APIResourceError('评论不能为空', 'Comment Can Not Be None')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceError('该文章异常，无法评论')
    comment = Comment(blog_id=blog.id, user_id=user.id, user_name=user.name, user_image=user.image,
                      content=content.strip())
    await comment.save()
    return comment


@post('/api/new/son/comment/from/blog/{id}')
async def api_new_son_comment(id, request, *, comment_id, content):
    user = request.__user__
    if user is None:
        raise APIResourceError('请先登陆', 'No User')
    if not comment_id:
        raise APIResourceError('评论异常，请联系管理员', 'No User')
    if not content or not content.strip():
        raise APIResourceError('评论不能为空', 'Comment Can Not Be None')
    blog = await Blog.find(id)
    if blog is None:
        raise APIResourceError('该文章异常，无法评论')
    comment = SonComment(blog_id=blog.id, user_id=user.id, user_name=user.name,
                         content=content.strip(), comment_id=comment_id)
    await comment.save()
    return comment


@post('/api/drop/comment/from/blog/{id}')
async def api_drop_comment(id, request):
    check_admin(request)
    c = await Comment.find(id)
    if c is None:
        raise APIResourceError('该评论状态异常', 'Comment Is Abnormal')
    sons = await SonComment.findAll('comment_id=?', [c.id])
    for son in sons:
        await son.remove()
    await c.remove()
    return dict(id=id)


@get('/api/get/comments')
async def api_get_comments(*, page=1):
    page_index = get_page_index(page)
    num = await User.findNumber('count(id)')
    p = Pager(num, page_index)
    if num == 0:
        return dict(page=0, comments=())
    comments = await Comment.findAll(orderBy='created_at desc', limit=(p.offset, p.limit))
    for c in comments:
        c.html_content = text2html(c.content)
    return dict(page=p, comments=comments)


@post('/api/find/blog/by/engine')
async def api_find_blog_by_engine(*, user_input):
    result = SimEngine.search(user_input)
    if not result:
        return dict(error='未查询到相关补给资源~')
    results = re.sub('\[(.*)\]', '(\\1)', str(result))
    blogs = await Blog.findAll(where='id in %s' % results, orderBy='created_at desc', limit=(0, 10))
    return dict(blogs=blogs)


@get('/api/get/multi/statistic')
@miniCache()
async def api_get_multi_statistic(*, dbNames_and_collectionNames, limit=0):
    limit = int(limit[0]) if isinstance(limit, list) else limit
    now_date = get_now_datetime()
    res = {}
    res_list = []
    for di in json.loads(dbNames_and_collectionNames[0]):
        _date = now_date
        pre = None
        nums = []
        times = []
        for dbName, collectionName in di.items():
            collection = client[dbName][collectionName]
            for i in range(limit):
                query = process_commands(gte={"download_time": _date.timestamp()})
                count = await collection.count_documents(query)
                if i == 0:
                    pre = count
                    nums.append(count)
                    times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
                else:
                    nums.append(count - pre)
                    times.append('%s.%s.%s' % (_date.year, _date.month, _date.day))
                    pre = count
                _date = _date - timedelta(days=1)
            res.setdefault('times', times[::-1])
            res_list.append(dict(name=collectionName, data=nums[::-1], type='line'))
    res.setdefault('nums', res_list)
    return res


@get('/api/get/ziru/price/statistic')
async def api_get_ziru_price_statistic():
    res = {}
    dbNames_and_collectionNames = [{'housePrice': 'ziru'}]
    column = 'house_price'
    for di in dbNames_and_collectionNames:
        a, b, c, d, e = [0 for _ in range(5)]
        for dbName, collectionName in di.items():
            collection = client[dbName][collectionName]
            documents = collection.find({}, {column: 1})
            async for doc in documents:
                if doc[column] < 800:
                    a += 1
                elif doc[column] < 1500:
                    b += 1
                elif doc[column] < 2000:
                    c += 1
                elif doc[column] < 3000:
                    d += 1
                else:
                    e += 1
        res_list = [
            {'value': a, 'name': '0-800'},
            {'value': b, 'name': '800-1500'},
            {'value': c, 'name': '1500-2000'},
            {'value': d, 'name': '2000-3000'},
            {'value': e, 'name': '3000+'}
        ]
        res.setdefault('nums', res_list)
    return res


@get('/api/get/zufang/price/statistic')
@miniCache()
async def api_get_zufang_price_statistic():
    res = {}
    dbNames_and_collectionNames = [{'housePrice': 'ziru'}, {'zufang': 'fangtx'}]
    for di in dbNames_and_collectionNames:
        a, b, c, d, e = [0 for _ in range(5)]
        collectionName = ''
        for dbName, collectionName in di.items():
            collection = client[dbName][collectionName]
            column = 'house_price' if dbName == 'housePrice' else '租金'
            documents = collection.find({}, {column: 1})
            async for doc in documents:
                try:
                    price = int(doc[column])
                except:
                    continue
                if price < 800:
                    a += 1
                elif price < 1500:
                    b += 1
                elif price < 2000:
                    c += 1
                elif price < 3000:
                    d += 1
                else:
                    e += 1
        res_list = [
            {'value': a, 'name': '0-800'},
            {'value': b, 'name': '800-1500'},
            {'value': c, 'name': '1500-2000'},
            {'value': d, 'name': '2000-3000'},
            {'value': e, 'name': '3000+'}
        ]
        res.setdefault(collectionName, res_list)
    return res


def get_price(price):
    res = re.search('(\d+)-(\d+)', price)
    if res:
        low, hig = map(int, res.groups())
    else:
        low, hig = (0, 0)
    return (low + hig) // 2 * 1000


@get('/api/get/boss/salary/statistic')
async def api_get_boss_salary_statistic():
    res = {}
    dbNames_and_collectionNames = [{'job': 'boss'}]
    for di in dbNames_and_collectionNames:
        a, b, c, d, e = [0 for _ in range(5)]
        collectionName = ''
        for dbName, collectionName in di.items():
            collection = client[dbName][collectionName]
            column = 'job_salary'
            documents = collection.find({}, {column: 1})
            async for doc in documents:
                try:
                    price = get_price(doc[column])
                except:
                    continue
                if price < 5000:
                    a += 1
                elif price < 10000:
                    b += 1
                elif price < 15000:
                    c += 1
                elif price < 20000:
                    d += 1
                else:
                    e += 1
        res_list = [
            {'value': a, 'name': '0-5000'},
            {'value': b, 'name': '5000-10000'},
            {'value': c, 'name': '10000-15000'},
            {'value': d, 'name': '15000-20000'},
            {'value': e, 'name': '20000+'}
        ]
        res.setdefault(collectionName, res_list)
    return res


@get('/monitor')
async def monitor():
    r = web.HTTPFound('http://47.101.42.79:8000')
    return r


@get('/get/init/anti/cookie')
async def anti_sipder_dom(request):
    webResponse = web.HTTPFound('/anti_spider')
    webResponse.set_cookie(ANTI_COOKIE, 'True', max_age=86400)
    webResponse.content_type = 'application/json'
    webResponse.body = json.dumps({'anti_spider': 'True'}, ensure_ascii=False).encode()
    return webResponse


@get('/anti_spider')
async def anti_spider_dom(request):
    return {'__template__': 'anti_spider.html'}
