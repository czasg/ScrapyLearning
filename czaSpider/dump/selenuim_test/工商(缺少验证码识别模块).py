import requests
import base64
import time
import random
import logging

from PIL import Image
from io import BytesIO
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

logging.basicConfig(format="%(asctime)s %(funcName)s[lines-%(lineno)d]: %(message)s")
logger = logging.getLogger(__name__)

THRESHOLD = 60
LEFT = 60
BORDER = 0


def get_anle_data(body):
    return ''


class BaseFunc:
    browser = None
    wait = None

    def get_screenshot(self):
        screenshot = self.browser.get_screenshot_as_png()
        return Image.open(BytesIO(screenshot))

    def get_gap(self, image1, image2):
        for i in range(LEFT, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    return i
        return LEFT

    def is_pixel_equal(self, image1, image2, x, y):
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        if abs(pixel1[0] - pixel2[0]) < THRESHOLD and abs(pixel1[1] - pixel2[1]) < THRESHOLD and abs(
                pixel1[2] - pixel2[2]) < THRESHOLD:
            return True
        else:
            return False

    def get_track(self, distance):
        track = []
        current = 0
        mid = distance * 2 / 3
        t = 0.2
        v = 0
        distance += 10
        while current < distance:
            if current < mid:
                a = random.randint(1, 3)
            else:
                a = -random.randint(3, 5)
            v0 = v
            v = v0 + a * t
            move = v0 * t + 0.5 * a * t * t
            current += move
            track.append(round(move))
        for i in range(2):
            track.append(-random.randint(2, 3))
        for i in range(2):
            track.append(-random.randint(1, 4))
        return track

    def get_slider(self):
        return self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "geetest_slider_button")))

    def move_to_gap(self, button, track):
        ActionChains(self.browser).click_and_hold(button).perform()
        for i in track:
            ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()
            time.sleep(0.0005)
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()


class GongShang(BaseFunc):
    def __init__(self, search, debug=False):
        self.search = search
        self.url = "http://www.gsxt.gov.cn/index.html"
        options = webdriver.ChromeOptions()
        # 设置为开发者模式，避免被识别
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        None if debug else options.add_argument('--headless')
        self.browser = webdriver.Chrome('old-chromedriver.exe', options=options)
        self.wait = WebDriverWait(self.browser, 20)
        self.search_type = None

    def __del__(self):
        self.browser.close()

    def browser_open(self):
        self.browser.get(self.url)

    def browser_search(self):
        search = self.wait.until(EC.element_to_be_clickable((By.ID, 'keyword')))
        submit = self.wait.until(EC.element_to_be_clickable((By.ID, 'btn_query')))
        time.sleep(2)
        search.clear()
        search.send_keys(self.search)
        logger.info('输入搜索词')
        time.sleep(2)
        submit.click()
        logger.info('已点击搜索')

    def open_and_search(self):
        self.browser_open()
        self.browser_search()

    def get_click_img(self):
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".geetest_item_img")))
        submit = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.geetest_commit_tip')))
        element = self.browser.find_element_by_xpath('//*[@class="geetest_item_img"]')
        self.find_type = 0
        json_data = get_anle_data(requests.get(element.get_attribute('src')).content)['message']['location']
        for data in json_data:
            ActionChains(self.browser).move_to_element_with_offset(element, data['x'], data['y']).click().perform()
            time.sleep(1)
        submit.click()
        return

    def get_slide_img(self, full=True):
        img = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "canvas.geetest_canvas_slice")))
        fullbg = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "canvas.geetest_canvas_fullbg")))
        self.find_type = 1
        if full:
            self.browser.execute_script(
                'document.getElementsByClassName("geetest_canvas_fullbg")[0].setAttribute("style", "")')
        else:
            self.browser.execute_script(
                "arguments[0].setAttribute(arguments[1], arguments[2])", fullbg, "style", "display: none")
        location = img.location
        size = img.size
        top, bottom, left, right = location["y"], location["y"] + \
                                   size["height"], location["x"], location["x"] + size["width"]
        screenshot = self.get_screenshot()
        captcha = screenshot.crop(
            (left, top, right, bottom))
        size = size["width"] - 1, size["height"] - 1
        captcha.thumbnail(size)
        return captcha

    def check_search_type(self):
        if self.search_type is None:
            while True:
                try:
                    logger.info('尝试点击获取')
                    self.get_click_img()
                    self.search_type = 0
                    logger.info('点击获取成功')
                    return
                except TimeoutException:
                    try:
                        logger.info('尝试滑块获取')
                        return self.get_slide_img()
                    except TimeoutException:
                        logger.info('尝试重新点击')
                        self.browser_search()
        else:
            return self.get_slide_img(False)

    def start(self, try_again=True):
        self.open_and_search()
        result1 = self.check_search_type()
        if result1:
            result2 = self.check_search_type()
            gap = self.get_gap(result1, result2)
            track = self.get_track(gap - BORDER)
            slider = self.get_slider()
            self.move_to_gap(slider, track)

        try:
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.search_logo_100000')))
            element = self.browser.find_element_by_xpath('//*[@class="search_list_item db"][1]')
            return element.get_attribute('href') if element.is_enabled() else None
        except NoSuchElementException:
            return '未获取到公司'
        except:
            logger.info('获取失败，重新尝试')
        self.search_type = None
        return self.start(try_again=False) if try_again else '未获取到公司'


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    start = time.time()
    search = '北京数博科技有限责任公司'  # 555555555 北京数博科技有限责任公司 武汉数博科技
    test = GongShang(search, debug=True)
    print(test.start())
    print(time.time() - start)
