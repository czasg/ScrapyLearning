from selenium import webdriver  # 提供webDriver支持
from selenium.webdriver.common.keys import Keys  # 提供键盘按键支持
"""
http://npm.taobao.org/mirrors/chromedriver/
下载chromedriver.exe
option = webdriver.ChormeOptions()  # 可添加配置命令行
option.add_argument()
driver = webdriver.Chorme(options=option)
保存登陆的两种方式：options和cookie
还有一种就是使用driver.add_cookie()
delete_cookie()、get_cookies()

driver.title
driver.current_url

driver.get()
driver.find_element_by_*
driver.get_cookies()

elem.clear()
elem.send_keys()
elem.send_keys(Keys.RETURN)

from selenium.webdriver.support.ui import Select
select = Select(driver.find_element_by_name("name"))
select.select_by_index(index)
select.select_by_visible_text("text")
select.select_by_value(value)

from selenium.webdriver import ActionChains  # 拖放一个元素
action_chains = ActionChains(driver)
action_chains.drag_and_drop(element, target).perform()
action_chains.move_to_element(menu).click(hidden_submenu).perform()
click()
click_and_hold()
.drag_and_drop_by_offset()  # 通过偏移量拖放
move_to_element_with_offset()  # 移动到具有偏移量的元素
tt = switch_to_alert()  # 捕捉弹框
print(tt.text)  # 打印弹框中的文本
tt.accept()  # 点击弹框中的ok
"""
driver = webdriver.Chrome("chromedriver123.exe")  # 创建一个chorme实例
driver.get("http://www.python.org")  # 打开目标url，等待加载完毕
assert "Python" in driver.title  # 检查打开页面的标题属性
elem = driver.find_element_by_name("q")  # 找到输入框
elem.clear()  # 清除输入框的内容
elem.send_keys("pycon")  # 在输入框中输入文本
elem.send_keys(Keys.RETURN)  # 模拟键盘输入回车键
assert "No results found." not in driver.page_source  # 检查整个页面资源
driver.close()  # quit关闭整个浏览器，close只会关闭一个标签页

"""
等待页面加载
隐式等待 -- 直接让webDriver等待一定时间后才执行
from selenium import webdriver
driver = webdriver.Chorme()
driver.implicitly_wait(10)  # 隐式等待10s，也就是强行等
driver.get(url)
myDynamicElement = driver.find_element_by_id("AIM")





显示等待 -- 等满足一定条件后再进行下一步的执行
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_condition as EC
driver = webdriver.Chorme()
driver.get(url)
try:
    elem = WebDriverWait(
        driver, 10)  # 在抛出异常之前等待10s，在10s内发现了查找元素，则继续执行
        .until(
            EC.presence_of_element_located((By.ID, "myDynamicElement")))
finally:
    driver.quit()
    

from selenium.webdriver.support import expected_conditions as EC
wait = WebDriverWait(driver, 10)
elem = wait.until(EC.element_to_be_clickable((By.ID, "someid")))
# expected_conditions 模块提供了一组预定义的条件供WebDriverWait使用
"""