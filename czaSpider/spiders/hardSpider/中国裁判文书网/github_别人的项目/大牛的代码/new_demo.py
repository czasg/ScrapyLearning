"""
新版文书网的demo(2019-09-01后的)
"""
import json
from datetime import datetime
from urllib import parse

import requests

from 大牛的代码.wenshu_utils import CipherText
from 大牛的代码.wenshu_utils import des3decrypt
from 大牛的代码.wenshu_utils import PageID
from 大牛的代码.wenshu_utils import RequestVerificationToken
from 大牛的代码.util_20190901 import get_postData

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

        result = self._request(get_postData('偷窃'))
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
    # demo.detail_page()

"""
99be82dd85264550af1aaaca00c06da8
692902dbddd44d3aa8bdaac40123726a
64e27bd0ce834bf2a39faac000c0f190
4e00b8ae589b4288a725aabe00c0e683
184eedc80c3b4f349349aaca00c06d96
"""

    # json_data = {
    #     'result': "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",
    #     'secretKey': 'YDQJBBsfQsKIvBUo1I8vCr1w'
    # }
    #
    # result = des3decrypt(cipher_text=json_data["result"],
    #             key=json_data["secretKey"],
    #             iv=datetime.now().strftime("%Y%m%d"))
    # print(result)