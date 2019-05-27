from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "world-test"

    url = "https://etax.xinjiang.chinatax.gov.cn/yhs-web/api/zdwfaj/ajlbcx"

    def start_requests(self):
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
        }
        data = {"nsrsbh": "", "nsrmc": "", "fddbrxm": "", "pageSize": 10, "sswfrlx": "00", "pageIndex": 1}
        yield Request(self.url, body=json.dumps(data), method="POST", headers=headers)

    def parse(self, response):
        print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
