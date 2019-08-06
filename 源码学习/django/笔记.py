__file__ = 'note'

"""
from django.http import HttpResponse  # 常规的返回，HttpResponse('hello world')
from django.shortcuts import render  # render是渲染模板，return render(request, 'home.html', {'string': string})
from django.urls import reverse  # reverse 接收 url 中的 name 作为第一个参数   reverse('add2', args=(4,5))
from django.http import HttpResponseRedirect  # 
from django.conf.urls import include, url

request.GET['a'] / request.GET.get('a', 0)

from app import view as app_view
urlpatterns = [
    path('add/', app_views.add, name='add')
]

//test?a=1&b=2
def test(request): request.GET.get('a', 0)

//test/a/b
path('add/<int:a>/<int:b>/', app_views.test2, name='test2')
def test2(request, a, b)

name 可以用于在 templates, models, views ……中得到对应的网址，相当于“给网址取了个名字”，只要这个名字不变，网址变了也能通过名字获取到

reverse('add2', args=(4,5))
不带参数的：
{% url 'name' %}
带参数的：参数可以是变量名
{% url 'name' 参数 %}
例如：
<a href="{% url 'add2' 4 5 %}">link</a>

HttpResponseRedirect    网址发生改变，在继承旧版的基础上
def old_add2_redirect(request, a, b):
    return HttpResponseRedirect(
        reverse('add2', args=(a, b))
    )
url(r'^add/(\d+)/(\d+)/$', calc_views.old_add2_redirect),
url(r'^new_add/(\d+)/(\d+)/$', calc_views.add2, name='add2'),


{{ item }}{% if not forloop.last %},{% endif %} 是最后一项其为真，否则为假，
forloop.first	当遍历的元素为第一项时为真
forloop.last	当遍历的元素为最后一项时为真
forloop.parentloop	 用在嵌套的 for 循环中， 获取上一层 for 循环的 forloop

{% for athlete in athlete_list %}
    <li>{{ athlete.name }}</li>
{% empty %}   列表中可能为空值时用 for  empty
    <li>抱歉，列表为空</li>
{% endfor %}



{{ request.user }} 获取当前用户：
如果登陆就显示内容，不登陆就不显示内容：
{% if request.user.is_authenticated %}
    {{ request.user.username }}，您好！
{% else %}
    请登陆，这里放登陆链接
{% endif %}
{{ request.path }}获取当前网址：
{{ request.GET.urlencode }}获取当前 GET 参数：


网址上就会显示出：/add/4/5/ 这个网址，假如我们以后修改 urls.py 中的r'^jiafa/(\d+)/(\d+)/$'，这样，我们不需要再次修改模板，当再次访问的时候，网址会自动变成 /jiafa/4/5/
# urls.py
urlpatterns = patterns('',
    url(r'^add/(\d+)/(\d+)/$', 'app.views.add', name='add'),
)

# template html
{% url 'add' 4 5 %}


objects = models.Manager()  # 如果不存在objects对象

Person.objects.create(name="WeizhongTu", age=24)  新建了一个用户WeizhongTu 那么如何从数据库是查询到它呢
Person.objects.get(name="WeizhongTu")

models:
pub_date = models.DateTimeField(u'发表时间', auto_now_add=True, editable = True)
update_time = models.DateTimeField(u'更新时间',auto_now=True, null=True)


admin.py
from django.contrib import admin
from .models import Article, Person
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'update_time',)
class PersonAdmin(admin.ModelAdmin):
    list_display = ('full_name',)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Person, PersonAdmin)

1.定制加载的列表, 根据不同的人显示不同的内容列表，比如输入员只能看见自己输入的，审核员能看到所有的草稿，这时候就需要重写get_queryset方法
class MyModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super(MyModelAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            return qs.filter(author=request.user)
2.定制搜索功能（django 1.6及以上才有) queryset 是默认的结果，search_term 是在后台搜索的关键词
class PersonAdmin(admin.ModelAdmin):
    list_display = ('name', 'age')
    search_fields = ('name',)
 
    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super(PersonAdmin, self).get_search_results(request, queryset, search_term)
        try:
            search_term_as_int = int(search_term)
            queryset |= self.model.objects.filter(age=search_term_as_int)
        except:
            pass
        return queryset, use_distinct
"""

"""QuerySet

新建一个对象的方法有以下几种：
Person.objects.create(name=name,age=age)
-----------------------------------
p = Person(name="WZ", age=23)
p.save()
-----------------------------------
p = Person(name="TWZ")
p.age = 23
p.save()
-----------------------------------
Person.objects.get_or_create(name="WZT", age=23)
这种方法是防止重复很好的方法，但是速度要相对慢些，返回一个元组，第一个为Person对象，第二个为True或False, 新建时返回的是True, 已经存在时返回False.



获取对象有以下方法：
Person.objects.all()
-----------------------------------
Person.objects.all()[:10] 切片操作，获取10个人，不支持负索引，切片可以节约内存
-----------------------------------
Person.objects.get(name=name)
get是用来获取一个对象的，如果需要获取满足条件的一些人，就要用到filter
-----------------------------------
Person.objects.filter(name="abc")  # 等于Person.objects.filter(name__exact="abc") 名称严格等于 "abc" 的人
-----------------------------------
Person.objects.filter(name__iexact="abc")  # 名称为 abc 但是不区分大小写，可以找到 ABC, Abc, aBC，这些都符合条件
-----------------------------------
Person.objects.filter(name__contains="abc")  # 名称中包含 "abc"的人
-----------------------------------
Person.objects.filter(name__icontains="abc")  #名称中包含 "abc"，且abc不区分大小写
-----------------------------------
Person.objects.filter(name__regex="^abc")  # 正则表达式查询
-----------------------------------
Person.objects.filter(name__iregex="^abc")  # 正则表达式不区分大小写
-----------------------------------
filter是找出满足条件的，当然也有排除符合某条件的
-----------------------------------
Person.objects.exclude(name__contains="WZ")  # 排除包含 WZ 的Person对象
-----------------------------------
Person.objects.filter(name__contains="abc").exclude(age=23)  # 找出名称含有abc, 但是排除年龄是23岁的

3、删除符合条件的结果
Person.objects.filter(name__contains="abc").delete() # 删除 名称中包含 "abc"的人
如果写成 
people = Person.objects.filter(name__contains="abc")  # 可以这样用吗，那不是还能修改吗
people.delete()
效果也是一样的，Django实际只执行一条 SQL 语句。


4、更新某个内容
(1) 批量更新，适用于 .all()  .filter()  .exclude() 等后面 (危险操作，正式场合操作务必谨慎)
Person.objects.filter(name__contains="abc").update(name='xxx') #秀碧，居然真的可以。 名称中包含 "abc"的人 都改成 xxx
Person.objects.all().delete() # 删除所有 Person 记录
(2) 单个 object 更新，适合于 .get(), get_or_create(), update_or_create() 等得到的 obj，和新建很类似。
twz = Author.objects.get(name="WeizhongTu")
twz.name="WeizhongTu"
twz.email="tuweizhong@163.com"
twz.save()  # 最后不要忘了保存！！！

注意事项：

(1). 如果只是检查 Entry 中是否有对象，应该用 Entry.objects.all().exists()

(2). QuerySet 支持切片 Entry.objects.all()[:10] 取出10条，可以节省内存

(3). 用 len(es) 可以得到Entry的数量，但是推荐用 Entry.objects.count()来查询数量，后者用的是SQL：SELECT COUNT(*)

(4). list(es) 可以强行将 QuerySet 变成 列表


6. QuerySet 是可以用pickle序列化到硬盘再读取出来的
>>> import pickle
>>> query = pickle.loads(s)     # Assuming 's' is the pickled string.
>>> qs = MyModel.objects.all()
>>> qs.query = query  

7. QuerySet 查询结果排序
作者按照名称排序
Author.objects.all().order_by('name')
Author.objects.all().order_by('-name') # 在 column name 前加一个负号，可以实现倒序

8. QuerySet 支持链式查询
Author.objects.filter(name__contains="WeizhongTu").filter(email="tuweizhong@163.com")
Author.objects.filter(name__contains="Wei").exclude(email="tuweizhong@163.com")

# 找出名称含有abc, 但是排除年龄是23岁的
Person.objects.filter(name__contains="abc").exclude(age=23)

9. QuerySet 不支持负索引
Person.objects.all()[:10] 切片操作，前10条
Person.objects.all()[-10:] 会报错！！！

# 1. 使用 reverse() 解决
Person.objects.all().reverse()[:2] # 最后两条
Person.objects.all().reverse()[0] # 最后一条

# 2. 使用 order_by，在栏目名（column name）前加一个负号
Author.objects.order_by('-id')[:20] # id最大的20条

10. QuerySet 重复的问题，使用 .distinct() 去重
# 去重方法
qs = qs.distinct()

"""

"""
1. 查看 Django queryset 执行的 SQL
 print str(Author.objects.all().query)  # 可以查看相关的sql语句 print str(Author.objects.filter(name="WeizhongTu").query)


2. values_list 获取元组形式结果
In [6]: authors = Author.objects.values_list('name', 'qq')  # [(u'WeizhongTu', u'336643078')
In [8]: list(authors)
如果只需要 1 个字段，可以指定 flat=True
In [9]: Author.objects.values_list('name', flat=True)
2.2 查询 twz915 这个人的文章标题
In [11]: Article.objects.filter(author__name='twz915').values_list('title', flat=True)

3. values 获取字典形式的结果
3.1 比如我们要获取作者的 name 和 qq
In [13]: Author.objects.values('name', 'qq')  # {'qq': u'915792575', 'name': u'twz915'},

values_list 和 values 返回的并不是真正的 列表 或 字典，也是 queryset，他们也是 lazy evaluation 的（惰性评估，通俗地说，就是用的时候才真正的去数据库查）


4. extra 实现 别名，条件，排序等
In [44]: tags = Tag.objects.all().extra(select={'tag_name': 'name'})


5. annotate 聚合 计数，求和，平均数等









"""

"""通用视图（类视图）
# 通用类的基类
from django.http import HttpResponse
from django.views.generic import View
class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello World')


from django.views.generic.base import TemplateView
from models import Article
class HomePageView(TemplateView):
    template_name = 'home.html'
    def get_content_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_articles'] = Article.object.all()[:5]  # 获取所有数据的前5???


from django.conf.urls import patterns, url
from django.views.generic.base import RedirectView
urlpatterns = patterns(
    path('', RedirectView.as_view(url='www.czasg.xyz'), name='cza')
)


from django.views.generic.detail import DetailView
from django.utils import timezone
from models import Article
class ArticleDetailView(DetailView):
    model = Article  # 要显示详情内容的类
    template_name = 'article_detail.html'
    def get_context_data(self, **kwargs):  # 在 get_context_data()函数中可以用于传递一些额外的内容到网页
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.new()
        return context
<html>
    <h1>标题：{{ object.title }}</h1>
    <p>内容：{{ object.content }}</p>
    <p>发表人: {{ object.reporter }}</p>
    <p>发表于: {{ object.pub_date|date }}</p>
    <p>日期: {{ now|date }}</p>
</html>


from django.views.generic.list import ListView
class ArticleListView(ListView):
    model = Article
    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
<html>
    <h1>文章列表</h1>
    <ul>
    {% for article in object_list %}
        <li>{{ article.pub_date|date }} - {{ article.headline }}</li>
    {% empty %}
        <li>抱歉，目前还没有文章。</li>
    {% endfor %}
    </ul>
</html>


"""

"""上下文渲染器
有时候我们想让一些内容在多个模板中都要有，比如导航内容，我们又不想每个视图函数都写一次这些变量内容，怎么办呢？
在模板中加入通用视图的意思嘛
context_processor.py
from django.conf import settings as original_settings
def settings(request):
    return {'settings': original_settings}
def ip_address(request):
    return {'ip_address': request.META['REMOTE_ADDR']}
"""

"""中间件
每一个请求都先通过中间件的process_request函数，该函数返回None或者HttpResponse对象。前者继续处理中间件，后者则直接返回
还有 process_view, process_exception 和 process_template_response 函数。
class CommonMiddleware:
    def process_request(self, request):
        return None
    def process_response(self, request, response):
        return response


class BlockedIpMiddleware:
    def process_request(self, request):
        if request.META['REMOTE_ADD'] = in getattr(settings, 'BLOCK_IP', []):
            return http.HttpResponseForbidden('<h1>Forbidden</h1>')
# 从上往下依次执行process_request函数，然后再倒叙依次执行process_response函数
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
]


import sys
from django.views.debug import technical_500_response
from django.conf import settings
class UserBaseExceptionMiddleware:
    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDRESS') in settings.INTERNAL_IP:
            return technical_500_response(request, *sys.exc_info())

"""
def main0():
    from functools import lru_cache

    from functools import wraps
    def cached(func):
        func.cache = {}

        @wraps(func)
        def wrapper(*args):
            try:
                return func.cache[args]
            except KeyError:
                func.cache[args] = result = func(*args)
                return result

        return wrapper

    @cached
    def add(x, y):
        print("calculating: %s + %s" % (x, y))
        return x + y

    @cached
    def test1(x, y):
        print("test1 calculating: %s + %s" % (x, y))
        return x + y

    @cached
    def test2(x, y):
        print("test2 calculating: %s + %s" % (x, y))
        return x + y

    print(add(1, 2))
    print(add(1, 2))
    print(test1(1, 2))
    print(add(1, 2))
    print(test1(1, 2))
    print(test2(1, 2))
    print(add(1, 2))


def main1():
    import weakref, collections

    class LocalCache():
        notFound = object()

        # list dict等不支持弱引用，但其子类支持，故这里包装了下
        class Dict(dict):
            def __del__(self):
                pass

        def __init__(self, maxlen=10):
            self.weak = weakref.WeakValueDictionary()
            self.strong = collections.deque(maxlen=maxlen)

        @staticmethod
        def nowTime():
            return int(time.time())

        def get(self, key):
            value = self.weak.get(key, self.notFound)
            if value is not self.notFound:
                expire = value[r'expire']
                if self.nowTime() > expire:
                    return self.notFound
                else:
                    return value
            else:
                return self.notFound

        def set(self, key, value):
            # strongRef作为强引用避免被回收
            self.weak[key] = strongRef = LocalCache.Dict(value)
            # 放入定大队列，弹出元素马上被回收
            self.strong.append(strongRef)

    # 装饰器
    from functools import wraps
    def funcCache(expire=0):
        caches = LocalCache()

        def _wrappend(func):
            @wraps(func)
            def __wrapped(*args, **kwargs):
                key = str(func) + str(args) + str(kwargs)
                result = caches.get(key)
                if result is LocalCache.notFound:
                    result = func(*args, **kwargs)
                    caches.set(key, {r'result': result, r'expire': expire + caches.nowTime()})
                    result = caches.get(key)
                return result

            return __wrapped

        return _wrappend

    # 测试函数
    import time
    @funcCache(expire=300)
    def test_cache(v):
        # 模拟任务处理时常3秒
        time.sleep(3)
        print('work 3s')
        return v

    print(test_cache(1))
    print(test_cache(2))

    print(test_cache(1))
    print(test_cache(2))
    print(test_cache(1))
    print(test_cache(2))

if __name__ == '__main__':  # sys.getrefcount(a) 查看弱引用计数
    # main0()
    main1()
