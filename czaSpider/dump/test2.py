# import os, re
# from datetime import datetime
#
# # 导入Fabric API:
# from fabric.api import *
#
# # 服务器登录用户名:
# env.user = 'czaorz'
# # sudo用户为root:
# env.sudo_user = 'root'
# # 服务器地址，可以有多个，依次部署:
# env.hosts = ['47.101.42.79']
#
# # 服务器MySQL用户名和口令:
# db_user = 'root'
# db_password = 'cza19950917'

from fabric.api import local

def prepare_deploy1():
    local("cd ..")
def prepare_deploy2():
    local("dir")
prepare_deploy1()
prepare_deploy2()