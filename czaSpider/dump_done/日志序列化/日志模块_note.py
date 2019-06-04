__goal__ = "test the package of logging"
"""总结就是：
日志最常规的就是logger=logging.getLogger(__name__)
然后设置日志级别logger.setLevel(logging.INFO)
这个很常规也很有用

然后就是功能多一点的模块logging.basicConfig()
这个可以设置日志的输出级别，输出样式
是否输出到文件，如果有输出到文件则不会在终端进行打印日志

最后就是我确实需要将日志输出到终端，也需要将日志输出到文件
使用Handler模块即可
from logging import Formatter, StreamHandler
from logging.handlers import TimedRotatingFileHandler
th = TimedRotatingFileHandler()
sh = StreamHandler()
logger.addHandler()将上面两个模块添加即可
"""

"""
logging.basicConfig(level=logging.DEBUG,
                    filename="test.log",
                    filemode="a",
                    format="%(asctime)s-[%s(funcName)s:%(lineno)d]-%(message)s")
%(name)s Logger的名字
%(levelno)s 数字形式的日志级别
%(levelname)s 文本形式的日志级别
%(pathname)s 调用日志输出函数的模块的完整路径名，可能没有
%(filename)s 调用日志输出函数的模块的文件名
%(module)s 调用日志输出函数的模块名
%(funcName)s 调用日志输出函数的函数名
%(lineno)d 调用日志输出函数的语句所在的代码行
%(created)f 当前时间，用UNIX标准的表示时间的浮 点数表示
%(relativeCreated)d 输出日志信息时的，自Logger创建以 来的毫秒数
%(asctime)s 字符串形式的当前时间。默认格式是 “2003-07-08 16:49:45,896”。逗号后面的是毫秒
%(thread)d 线程ID。可能没有
%(threadName)s 线程名。可能没有
%(process)d 进程ID。可能没有
%(message)s用户输出的消息

如果加了filename和filemode，name就不会输出到终端，而是直接将日志输出到文件了
常用的几个样式：asctime，name，funcName，lineno，message
这个其实是可以固定下来的，以后不出意外的话，可以只用这套模板
format="%(asctime)s - [%(name)s.%(funcName)s : %(lineno)d] - %(message)s"


如果你想既往终端输入，也往日志文件里输入，可以使用其他模块
Logger：输出到终端
Handler：输出到文件
Filter：日志过滤
Formatter：日志布局

我们可以先设置logger=logging.getLogger(__name__)
然后不进行设置basicConfig，而是转而设置handler，如from logging import handlers
handlers.TimeRotatingFileHandler(filename="text.log",
                                 when=when,
                                 backupCount=backCount,
                                 encoding="utf-8")
when是间隔的时间单位，有以下几种：
# S 秒
# M 分
# H 小时、
# D 天、
# W 每星期（interval==0时代表星期一）
# midnight 每天凌晨
backupCount是备份文件的个数
然后我们只需要添加这个handler就行了
logger.addHandler(handler)

sh = StreamHandler() # 往屏幕上输出
sh.setFormatter(format_str) # 设置屏幕上显示的格式

th = TimedRotatingFileHandler()# 往文件中输出
th.setFormatter(format_str)

logger.addHandler(sh)
logger.addHandler(th)
"""

# import logging
#
# logging.basicConfig(level=logging.DEBUG,
#                     format="%(asctime)s - [%(name)s.%(funcName)s : %(lineno)d] - %(message)s")
# logger = logging.getLogger(__name__)
#
#
# def hello():
#     logger.debug("hello world")
#     logger.info("hello world")
#     logger.warning("hello world")
#     logger.error("hello world")
#     logger.critical("hello world")
# hello()


# import logging
# from logging import Formatter, StreamHandler
# from logging.handlers import TimedRotatingFileHandler
#
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# th = TimedRotatingFileHandler(filename="hello.log",
#                               when="D",
#                               backupCount=3)
# sh = StreamHandler()
# formatter = Formatter("%(asctime)s - [%(name)s.%(funcName)s : %(lineno)d] - %(message)s")
# th.setFormatter(formatter)
# sh.setFormatter(formatter)
# logger.addHandler(th)
# logger.addHandler(sh)
#
#
# def hello():
#     logger.debug("hello world")
#     logger.info("hello world")
#     logger.warning("hello world")
#     logger.error("hello world")
#     logger.critical("hello world")
# hello()
