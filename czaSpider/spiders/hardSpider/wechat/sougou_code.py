import json, datetime, base64, requests
import logging
import random
import re
from urllib.parse import unquote

from scrapy import Request, FormRequest

# from scrapyProj.tools import get_timestamp
# from scrapyProj.tools.captcha import get_code_from_captcha
# from scrapyProj.tools.cookie import set_redis_cookie_jar

COOKIE_CACHE_NAME_FOR_SOGOU = "wechat_sougou"

def get_timestamp(len=13):
    if len < 10:
        return "0"
    return str(int(datetime.datetime.timestamp(datetime.datetime.now()) * (10 ** (len - 10))))
def get_code_from_captcha(content, model=None, is_b64=False, url=None):
    url = url or "http://192.168.0.166:19952/captcha/v1"
    bb = content if is_b64 else base64.b64encode(content).decode()
    data = {"image": bb}
    if model:
        data["model_site"] = model
    res = requests.post(url, headers={"Content-Type": "application/json"}, json=data)
    info = json.loads(res.text)
    return info["message"]
class CodeBase:
    name = None
    retry_limit = 5

    @classmethod
    def need_code(cls, spider, response):
        raise NotImplementedError("need_code must be implemented and return bool")

    def __init__(self, spider, response):
        assert self.name, "反验证码类必须有个名字"
        self.spider = spider
        self.logger = logging.getLogger(self.name + "验证码处理")
        self.logger.warning("触发反爬-" + self.name)
        self.referer = response.url
        self.callback = response.request.callback
        self.retry_count = 0

    def parse_anti_spider(self):
        if self.retry_count >= self.retry_limit:
            self.logger.error(self.name + "验证码识别超限")
            return
        self.retry_count += 1
        self.logger.info("第%d次尝试识别%s验证码" % (self.retry_count, self.name))
        yield from self.request_img()

    def request_img(self):
        raise NotImplementedError("how you fetch captcha")

    def process_img(self, response):
        raise NotImplementedError("process_img should process the img fetched")

    @classmethod
    def deco(cls, func):
        def wrapper(spider, response):
            if cls.need_code(spider, response):
                code_obj = cls(spider, response)
                yield from code_obj.parse_anti_spider()
                return
            yield from func(spider, response)

        return wrapper


class SogouCode(CodeBase):
    # weixin.sogou验证码处理
    name = "搜狗页面"

    _img_url = "https://weixin.sogou.com/antispider/util/seccode.php?tc="
    thank_url = "https://weixin.sogou.com/antispider/thank.php"

    def __init__(self, response):
        super().__init__(response)
        self.r = re.search("from=([^&]+)", response.url).group(1)
        self.url = response.urljoin(unquote(self.r))

    @property
    def img_url(self):
        return self._img_url + get_timestamp(10)

    @classmethod
    def need_code(cls, spider, response):
        return "antispider" in response.url

    def request_img(self):
        yield Request(self.img_url, self.process_img)

    def process_img(self, response):
        code = get_code_from_captcha(response.body)
        self.logger.info("验证码计算结果%s" % code)
        data = {"r": self.r, "v": "5", "c": code}
        yield FormRequest(self.thank_url, formdata=data, callback=self.re_request)

    def re_request(self, response):
        info = json.loads(response.text)
        if info["code"] == 0:
            cookies = {
                "SUV": get_timestamp() + "%03d" % (random.random() * 1000),  # 13位时间戳+3位随机数
                "SNUID": info["id"],  # id
            }
            self.spider.log('获取到了微信cookie：%s' % json.dumps(cookies, ensure_ascii=False), level=logging.INFO)
            yield Request(self.url, self.callback, dont_filter=True, headers={"Referer": self.referer}, cookies=cookies)
        else:
            self.logger.warning("验证码识别失败")
            yield from self.parse_anti_spider()


class WeixinCode(CodeBase):
    name = "微信页面"
    retry_limit = 3
    _img_url = "https://mp.weixin.qq.com/mp/verifycode?cert="
    report_url = "https://mp.weixin.qq.com/mp/verifycode"

    @property
    def img_url(self):
        cert = get_timestamp(17)
        cert = cert[:13] + "." + cert[13:]
        return self._img_url + cert

    @classmethod
    def need_code(cls, spider, response):
        return "为了保护你的网络安全，请输入验证码" in response.text

    def request_img(self):
        yield Request(self.img_url, self.process_img)

    def process_img(self, response):
        code = get_code_from_captcha(response.body)
        self.logger.info("验证码计算结果%s" % code)
        cert = re.search("cert=([^=&]+)", response.url).group(1)
        data = {"input": code, "appmsg_token": "", "cert": cert}
        yield FormRequest(self.report_url, self.v_parse3, formdata=data)

    def v_parse3(self, response):  # 识别完成后跳转到正常页面
        info = json.loads(response.text)
        if "ret" in info and info["ret"] == 0:
            yield Request(self.referer, self.callback, dont_filter=True)
        else:
            self.logger.warning("验证码识别失败")
            yield from self.parse_anti_spider()
