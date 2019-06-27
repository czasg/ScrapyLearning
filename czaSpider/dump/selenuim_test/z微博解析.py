__file__ = '微博'

"""首先是刷新cookie
提供账号与密码，进行登录，获取该账号的cookie，此cookie可进行后续爬取

# 导包
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # 期待某些元素出现
from selenium.webdriver.support.ui import WebDriverWait

# 初始化配置
options = webdriver.ChromeOptions()  # 添加可配置命令行
options.add_argument('--headless')  # 配置headless
browser = webdriver.Chrome(chrome_options=options)  # 获取浏览器操作对象
browser.set_window_size(1050, 840)  # 定义窗口大小
wait = WebDriverWait(browser, 20)

# 登录页面
browser.get('https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/')  # 进入登录页面
time.sleep(1)  # 这个时延还是要的
username = wait.until(EC.presence_of_element_located((By.ID, 'loginName')))  # 在wait等待时间内，等待出现该元素，未出现则报错
password = wait.until(EC.presence_of_element_located((By.ID, 'loginPassword')))  # 在wait等待时间内，等待出现该元素，未出现则报错
submit = wait.until(EC.element_to_be_clickable((By.ID, 'loginAction')))  # 在wait等待时间内，等待出现该元素并可点击，未出现则报错
username.send_keys(self.username)
password.send_keys(self.password)
submit.click()  # 完成登录
time.sleep(3.5)

# 获取cookie
cookie = {}
for elem in browser.get_cookies():
    cookie[elem["name"]] = elem["value"]

# 滑块验证码 -- 似乎不是必现的


"""

"""
import aircv as ac
imsrc = ac.imread('cap4.jpg')
imobj = ac.imread('cap2.png')
pos = ac.find_template(imsrc, imobj)
#返回值
#{'confidence': 0.5522063970565796, 'result': (557, 214), 'rectangle': ((489, 146), (489, 282), (625, 146), (625, 282))}
# result: 查找到的点
# rectangle： 目标图像周围四个点的坐标
# confidence: 查找图片匹配成功的特征点 除以 总的特征点
"""
