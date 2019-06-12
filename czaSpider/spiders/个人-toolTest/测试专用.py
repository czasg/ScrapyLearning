from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    def start_requests(self):
        formData = {
            'access_token': '',
            'local_province_id': '42',
            'local_type_id': '1',
            'page': '1',
            'school_id': '42',
            'signsafe': '905c301c8585745cff80dbb7e72c53d4',
            'size': '20',
            'uri': 'apidata/api/gk/score/special',
            'year': '2018'
        }
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Content-Type': 'application/json;charset=UTF-8',
            'Origin': 'https://gkcx.eol.cn',
            'Referer': 'https://gkcx.eol.cn/school/42/specialtyline?cid=0',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        }
        yield Request('https://api.eol.cn/gkcx/api/', body=json.dumps(formData),
                      method='POST',
                      headers=headers)

    def parse(self, response):
        print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
