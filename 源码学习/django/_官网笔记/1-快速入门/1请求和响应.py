__file__ = '请求和相应'

"""
python -m django --version
django-admin startproject mysite
python manage.py startapp polls
python manage.py runserver 0:8000

当包括其它 URL 模式时你应该总是使用 include() ， admin.site.urls 是唯一例外。

函数 path() 具有四个参数，两个必须参数：route 和 view，两个可选参数：kwargs 和 name
route：route 是一个匹配 URL 的准则（类似正则表达式）。当 Django 响应一个请求时，它会从 urlpatterns 的第一项开始，按顺序依次匹配列表中的项，直到找到匹配的项。
view：当 Django 找到了一个匹配的准则，就会调用这个特定的视图函数，并传入一个 HttpRequest 对象作为第一个参数，被“捕获”的参数以关键字参数的形式传入
kwargs：任意个关键字参数可以作为一个字典传递给目标视图函数
name：为你的 URL 取名能使你在 Django 的任意地方唯一地引用它，尤其是在模板中。这个有用的特性允许你只改一个文件就能全局地修改某个 URL 模式。
"""
