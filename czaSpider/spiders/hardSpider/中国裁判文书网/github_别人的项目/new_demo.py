"""
新版文书网的demo(2019-09-01后的)
"""
import json
from datetime import datetime
from urllib import parse

import requests

from wenshu_utils.cipher import CipherText
from wenshu_utils.des3 import des3decrypt
from wenshu_utils.pageid import PageID
from wenshu_utils.token import RequestVerificationToken

API = "http://120.78.76.198:8000/wenshu"


class NewDemo:
    url: parse.ParseResult = parse.urlparse("http://wenshu.court.gov.cn/website/parse/rest.q4w")

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        })
        # self.session.proxies = # TODO 配置你的代理

    def _request(self, data: dict) -> requests.Response:
        # response = requests.post(API, json={"path": self.url.path, "request_args": data})
        # if response.status_code != 200:
        #     raise Exception(response.text)
        # 
        # kwargs = response.json()

        response = self.session.post(self.url.geturl(), data=data)
        if response.status_code != 200:
            raise Exception(response.status_code)

        json_data = response.json()

        plain_text = des3decrypt(cipher_text=json_data["result"],
                                 key=json_data["secretKey"],
                                 iv=datetime.now().strftime("%Y%m%d"))

        result = json.loads(plain_text)
        return result

    def list_page(self):
        """文书列表页"""
        data = {
            "pageId": PageID(),
            "sortFields": "s50:desc",
            "ciphertext": CipherText(),
            "pageNum": 1,
            "pageSize": 5,
            "queryCondition": json.dumps([{"key": "s8", "value": "03"}]),  # 查询条件: s8=案件类型, 03=民事案件
            "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc",
            "__RequestVerificationToken": RequestVerificationToken(24),
        }

        result = self._request(data)
        print(result)

    def detail_page(self):
        """文书详情页"""
        data = {
            "docId": "4e00b8ae589b4288a725aabe00c0e683",
            "ciphertext": CipherText(),
            "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
            "__RequestVerificationToken": RequestVerificationToken(24),
        }

        result = self._request(data)
        print(result)


if __name__ == '__main__':
    demo = NewDemo()
    demo.list_page()
    demo.detail_page()
