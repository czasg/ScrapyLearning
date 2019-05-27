from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


url = 'https://passport.weibo.cn/signin/login?entry=mweibo&r=https://weibo.cn/'
web = webdriver.Chrome("chromedriver.exe")
waiter = WebDriverWait(web, 20)

web.get(url)
username = waiter.until(EC.presence_of_element_located((By.ID, 'loginName')))
password = waiter.until(EC.presence_of_element_located((By.ID, 'loginPassword')))
submit = waiter.until(EC.presence_of_element_located((By.ID, 'loginAction')))
username.send_keys('15607173521')
password.send_keys('cza19950917')
submit.click()
