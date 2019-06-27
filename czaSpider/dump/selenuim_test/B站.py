import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC  # 期待某些元素出现
from selenium.webdriver.support.ui import WebDriverWait

browser = webdriver.Chrome("chromedriver.exe")
browser.set_window_size(1050, 840)  # 定义窗口大小
wait = WebDriverWait(browser, 20)

browser.get('https://passport.bilibili.com/login')  # 进入登录页面
time.sleep(1)  # 这个时延还是要的
username = wait.until(EC.presence_of_element_located((By.ID, 'login-username')))  # 在wait等待时间内，等待出现该元素，未出现则报错
password = wait.until(EC.presence_of_element_located((By.ID, 'login-passwd')))  # 在wait等待时间内，等待出现该元素，未出现则报错
submit = wait.until(EC.element_to_be_clickable((By.XPATH, '//a[@class="btn btn-login"]')))  # 在wait等待时间内，等待出现该元素并可点击，未出现则报错
username.send_keys('15607173521')
password.send_keys('cza19950917')
submit.click()  # 完成登录
time.sleep(3.5)
