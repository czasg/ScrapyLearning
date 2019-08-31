import sys

from bypy import ByPy

bp = ByPy()

# bp.mkdir('/hello/')
# bp.mkdir(u'/你好/世界')
# bp.upload(localpath=u'bypy_help.txt', remotepath=u'hello/bypy_help.txt', ondup=u'overwrite')


# bp.download(remotepath=u'hello/bypy_help.txt',localpath=u'help_yun.txt')


print(bp.list(u'/file_server/'))