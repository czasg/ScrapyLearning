import sys

from bypy import ByPy

bp = ByPy()
bp.upload(localpath=u'bypy_help.txt', remotepath=u'pdf/bypy_help.txt', ondup=u'overwrite')
# bp.download(remotepath=u'a/bypy_help.txt',localpath=u'help_yun.txt')


# print(bp.list('/apps/bypy'))
