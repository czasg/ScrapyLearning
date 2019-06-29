import argparse
from importlib import import_module

"""
czaSpider.spiders.个人-toolTest.ziru-new cza_run_spider --myspider
"""

if __name__ == '__main__':
    try:
        parse = argparse.ArgumentParser(description='Start Scrapy')
        parse.add_argument('path', help='爬虫路径')
        parse.add_argument('func', help='待执行函数')
        parse.add_argument('args', nargs='*', help='参数')
        parse.add_argument("--myspider", "-m", help="是否引用MySpider", action="store_true")
        args = parse.parse_args()
        path, func, args, myspider = args.path, args.func, args.args, args.myspider
        module = import_module(path)
        if myspider:
            module = getattr(module, 'MySpider')
        getattr(module, func)(*args)
    except:
        pass
