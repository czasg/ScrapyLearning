__file__ = '临时笔记'

"""
from django.http import HttpResponse
HttpResponse 是把内容显示到网页上   -- 定义在views中

from django.conf.urls import patterns, include, url
path('admin/', admin.site.urls),  -- 定义在urls中

在views中的函数都只有一个request参数嘛
request.GET


from django.urls import reverse
reverse 接收 url 中的 name 作为第一个参数
我们在代码中就可以通过 reverse() 来获取对应的网址（这个网址可以用来跳转，也可以用来计算相关页面的地址），只要对应的 url 的name不改，就不用改代码中的网址。


HomePage.as_view()  这个as_view是什么意思
from django.views.generic import View
class WyPlay(View):  使用这种类似构造对象的方法来实现吗

"""