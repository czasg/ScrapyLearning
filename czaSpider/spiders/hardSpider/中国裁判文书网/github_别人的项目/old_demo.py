"""
旧版文书网的demo(2019-09-01前的)
"""
import json
from pprint import pprint

import requests

from wenshu_utils.old.docid.decrypt import decrypt_doc_id
from wenshu_utils.old.docid.runeval import decrypt_runeval
from wenshu_utils.old.document.parse import parse_detail
from wenshu_utils.old.vl5x.args import Vjkl5, Vl5x, Number, Guid


class OldDemo:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        })

    def list_page(self):
        """文书列表页"""
        url = "http://oldwenshu.court.gov.cn/List/ListContent"
        data = {
            "Param": "案件类型:刑事案件",
            "Index": 1,
            "Page": 10,
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": Vl5x(self.session.cookies.setdefault("vjkl5", Vjkl5())),
            "number": Number(),
            "guid": Guid(),
        }
        response = self.session.post(url, data=data)

        if response.status_code != 200:
            raise Exception(response.status_code)

        if response.content == b'"remind"':
            raise Exception("访问限制，请使用代理")

        if b"window.location.href" in response.content:
            raise Exception("需要验证码，请自行打码或使用代理")

        if "500错误".encode() in response.content:
            raise Exception("500错误，服务器繁忙")

        json_data = json.loads(response.json())
        print("列表数据:", json_data)

        runeval = json_data.pop(0)["RunEval"]
        try:
            key = decrypt_runeval(runeval)
        except ValueError as e:
            raise ValueError("返回脏数据") from e
        else:
            print("RunEval解析完成:", key, "\n")

        key = key.encode()
        for item in json_data:
            cipher_text = item["文书ID"]
            print("解密:", cipher_text)
            plain_text = decrypt_doc_id(doc_id=cipher_text, key=key)
            print("成功, 文书ID:", plain_text, "\n")

    def detail_page(self):
        """文书详情页"""
        url = "http://oldwenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
        params = {
            "DocID": "029bb843-b458-4d1c-8928-fe80da403cfe",
        }
        response = self.session.get(url, params=params)

        if response.status_code != 200:
            raise Exception(response.status_code)

        if b"window.location.href" in response.content:
            raise Exception("需要验证码，请自行打码或使用代理")

        if "500错误".encode() in response.content:
            raise Exception("500错误，服务器繁忙")

        group_dict = parse_detail(response.text)
        pprint(group_dict)


if __name__ == '__main__':
    demo = OldDemo()
    demo.list_page()
    demo.detail_page()
