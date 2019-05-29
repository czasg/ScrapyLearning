def hello():
    print("hello world")


def tar():
    local("tar -czvf test.tar.gz test.py")
    print("tar success")


def unpack():
    """
    c create新建
    x extract解压
    f file指定文件
    v view查看过程
    z 使用gzip捷星压缩或解压
    :return:
    """
    local("tar -xzvf test.tar.gz test.py")
    print("unpack success")


import os, re
from datetime import datetime

# 导入Fabric API:
from fabric.api import *

# 服务器登录用户名:
env.user = 'czaorz'
env.password = 'czasg0.0'
# sudo用户为root:
env.sudo_user = 'root'
# 服务器地址，可以有多个，依次部署:
# env.hosts = ['47.101.42.79']
env.hosts = ['47.101.42.79']

# 服务器MySQL用户名和口令:
db_user = 'root'
db_password = 'cza19950917'

_TAR_FILE = "test.tar.gz"


def build():
    includes = ["test1", "test2", "*py"]
    excludes = ["*.pyc"]
    local("ls -al")
    cmd = ['tar', '-czvf', '%s' % _TAR_FILE]
    cmd.extend(['--exclude=\'%s\'' % e for e in excludes])
    cmd.extend(includes)
    local(' '.join(cmd))
    print("Build Tar.Gz File Done!")

_REMOTE_TEM_TAR = "/test/%s" % _TAR_FILE
_REMOTE_BASE_DIR = "/test"

def deploy():
    # newdir = "test-%s" % datetime.now().strftime("%y-%m-%d_%H.%M.%S")
    # run("ls /")
    run("mkdir /home/czaorz/workplace/test")
