"""
Spider Middleware manager

See documentation in docs/topics/spider-middleware.rst
"""
import six
from twisted.python.failure import Failure
from scrapy.middleware import MiddlewareManager
from scrapy.utils.defer import mustbe_deferred
from scrapy.utils.conf import build_component_list

def _isiterable(possible_iterator):
    return hasattr(possible_iterator, '__iter__')

class SpiderMiddlewareManager(MiddlewareManager):

    component_name = 'spider middleware'

    @classmethod
    def _get_mwlist_from_settings(cls, settings):
        return build_component_list(settings.getwithbase('SPIDER_MIDDLEWARES'))  # 'scrapy.spidermiddlewares.httperror.HttpErrorMiddleware': 50,

    def _add_middleware(self, mw):  # 中加载好的中间件中获取你所需要的模块
        super(SpiderMiddlewareManager, self)._add_middleware(mw)
        if hasattr(mw, 'process_spider_input'):
            self.methods['process_spider_input'].append(mw.process_spider_input)
        if hasattr(mw, 'process_spider_output'):
            self.methods['process_spider_output'].appendleft(mw.process_spider_output)
        if hasattr(mw, 'process_spider_exception'):
            self.methods['process_spider_exception'].appendleft(mw.process_spider_exception)
        if hasattr(mw, 'process_start_requests'):
            self.methods['process_start_requests'].appendleft(mw.process_start_requests)

    def scrape_response(self, scrape_func, response, request, spider):
        fname = lambda f:'%s.%s' % (
                six.get_method_self(f).__class__.__name__,
                six.get_method_function(f).__name__)
        """他会先执行完某一函数的所有回调情况，再往下走????whats???? 似乎每一个爬虫流程都会走一遍，whats
        执行process_spider_input
        执行call_spider
        执行process_spider_output
        """
        def process_spider_input(response):
            for method in self.methods['process_spider_input']:
                try:
                    result = method(response=response, spider=spider)
                    assert result is None, \
                            'Middleware %s must returns None or ' \
                            'raise an exception, got %s ' \
                            % (fname(method), type(result))
                except:
                    return scrape_func(Failure(), request, spider)
            return scrape_func(response, request, spider)  # 这里就是call_spider爬虫处理后的结果，是一个dfd，里面指定了下一级的回调函数

        def process_spider_exception(_failure):  # 错了才会执行这里
            exception = _failure.value
            for method in self.methods['process_spider_exception']:
                result = method(response=response, exception=exception, spider=spider)
                assert result is None or _isiterable(result), \
                    'Middleware %s must returns None, or an iterable object, got %s ' % \
                    (fname(method), type(result))
                if result is not None:
                    return result
            return _failure

        def process_spider_output(result):
            for method in self.methods['process_spider_output']:
                result = method(response=response, result=result, spider=spider)
                assert _isiterable(result), \
                    'Middleware %s must returns an iterable object, got %s ' % \
                    (fname(method), type(result))
            return result

        dfd = mustbe_deferred(process_spider_input, response)  # 对进来的数据做一次处理???怎么还有这种操作
        dfd.addErrback(process_spider_exception)
        dfd.addCallback(process_spider_output)
        return dfd

    def process_start_requests(self, start_requests, spider):  # 这玩意早早的就执行了
        return self._process_chain('process_start_requests', start_requests, spider)
