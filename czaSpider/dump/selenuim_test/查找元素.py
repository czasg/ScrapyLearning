# -*-utf-8-*-
__author__ = "selenium"
"""
<input type="text" name="passwd" id="passwd-id" class="test"/>
elem = driver.find_element_by_id("passwd-id")
elem = driver.find_element_by_name("passwd")
elem = driver.find_element_by_xpath("//input[@id='passwd-id']")  这个无敌了，但是必须单匹配，不能多匹配
elem = driver.find_elements_by_xpath(xpath)
elem = driver.find_element_by_class_name("test")
elem = driver.find_element_by_tag_name("h1") # 通过标签名进行查找


from selenium.webdriver.common.by import By
driver.find_element(By.XPATH, "//button[text()="something"]")
driver.find_elements(By.XPATH, '//button')
By.ID
By.NAME
By.CLASS_NAME

# <a href="continue.html">Continue</a>
a = driver.find_element_by_link_text("Continue")
a = driver.find_element_by_partial_link_text("Con")
"""

"""使用下拉框
element = driver.find_element_by_xpath("//select[@name='name']")
all_options = element.find_elements_by_tag_name('option')
for o in all_options:
    option.click()

"""
