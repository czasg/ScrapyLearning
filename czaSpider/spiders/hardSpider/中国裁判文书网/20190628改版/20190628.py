import logging
import execjs
import requests
import re

from urllib.parse import urljoin

logger = logging.getLogger(__name__)


def downloaded(doc_url):
    error_num = 0
    while error_num < 3:
        with requests.session() as session:
            ua = None  # todo
            res = session.get(doc_url, headers={"User-Agent": ua})
            if re.search('eval\(function\(p,a,c,k,e,r', res.text):
                redirect_url = AntiJS.get_redirect_url_from_js(res.text)
                doc_url = urljoin(doc_url, redirect_url)
                res = session.get(doc_url, headers={"User-Agent": ua})
                if re.search('eval\(function\(p,a,c,k,e,r', res.text):
                    error_num += 1
                    logging.warning("第%d次尝试失败！" % error_num)
                    continue
            return res


class AntiJS:
    _sojson = None

    def __init__(self, spider, response):
        logger.warning("enter AntiJS...")
        self.spider = spider
        self.response = response
        self.callback = response.request.callback

    @classmethod
    def get_anti(cls):
        if not cls._sojson:
            logger.warning("get_anti")
            logger.warning("获取sojson.v5")
            with open('sojson.v5', encoding='utf-8') as f:
                js = f.read()
                cls._sojson = execjs.compile(js)
        return cls._sojson

    @classmethod
    def get_redirect_url_from_js(cls, javascript_code):
        anti_first = cls.get_anti()
        dynamicUrl, wzWsQuestion, wzWsFactor = \
            re.search('dynamicurl\|(.*?)\|.*?wzwsquestion\|(.*?)\|.*?wzwsfactor\|(.*?)\|',
                      javascript_code).groups()
        wzWsChallenge = anti_first.call('anti_first', wzWsQuestion, wzWsFactor)
        return dynamicUrl + "?wzwschallenge=" + wzWsChallenge

    def anti_first(self):
        javascript_code = self.response.text
        dynamicUrl = self.get_redirect_url_from_js(javascript_code)
        dynamicUrl = self.response.urljoin(dynamicUrl)
        yield self.response.request.replace(url=dynamicUrl, dont_filter=True)

    @classmethod
    def auto(cls, func):
        def wrapper(spider, response):
            if re.search('eval\(function\(p,a,c,k,e,r', response.text):
                anti = cls(spider, response)
                yield from anti.anti_first()
                logger.warning("Finished AntiJS...")
                return
            yield from func(spider, response)

        return wrapper
