import pkg_resources


def run_entry_point(data):
    group = 'package?'
    for entrypoint in pkg_resources.iter_entry_points(group=group):
        print('entrypoint:', entrypoint)
        plugin = entrypoint.load()
        plugin(data)

run_entry_point(100)

"""
# 在引擎正式启动，也就是爬虫crawl里执行yield engine.start时发送此信号
signals.engine_started

# 在执行一次调度的时候发送此信号
signals.request_scheduled

# 在调度的时候，请求指纹过滤，要是被过滤掉了，则发送此信息
signals.request_dropped


signals.engine_stopped

self._closewait.callback(None)  最中执行此函数，才会停止整个程序，这里的closewait才是对外的返回的 defer.Deferred() 对象
"""