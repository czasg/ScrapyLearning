import os

from datetime import datetime
from fabric.api import *

env.user = "czaorz"
env.sudo_user = "root"
env.hosts = ["47.101.42.79"]
db_user = "root"
db_password = "cza19950917"

_TAR_FILE = "check-test.tar.gz"

def build():
    includes = ["static","templates","*.py"]
    excludes = [".pyc"]
    with lcd(os.path.join(os.path.abspath('.'), "check")):
        cmd = ['tar', '-czvf', '../%s' % _TAR_FILE]
        cmd.extend(['--exclude=\'%s\'' % e for e in excludes])
        cmd.extend(includes)
        local(' '.join(cmd))

_REMOTE_TMP_TAR = "/test/%s" % _TAR_FILE
_REMOTE_BASE_DIR = "/test"

def deploy():
    newdir = "check-%s" % datetime.now().strftime("%y-%m-%d_%H.%M.%S")
    put("disk/%s" % _TAR_FILE, _REMOTE_TMP_TAR)
    # with cd("/test"):
    #     run("tar -xzvf %s" % _TAR_FILE)

"""
只需要做两件事情
1、压缩
2、推送

上面的也可以用git来完成，感觉也都差不多吧
剩下的解压，重ln连接，都是可以我自己操作的
"""




