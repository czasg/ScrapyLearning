import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

with open('zgcpwsw1.js', encoding='utf-8') as f:
    js = f.read()
    anti_first = execjs.compile(js)

with open('zgcpwsw2.js', encoding='utf-8') as f:
    js = f.read()
    anti_second = execjs.compile(js)

with open('zgcpwsw3.js', encoding='utf-8') as f:
    js = f.read()
    anti_third = execjs.compile(js)


class MySpider(IOCO):
    name = "chinaReferee-government"

    url = "http://wenshu.court.gov.cn/List/ListContent"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    formData = {
        "Param": "全文检索:处罚",
        "Index": "1",
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": "",
        "number": "",
        "guid": "",
    }

    def start_requests(self):
        entrance = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=3YHLPLNF" \
                   "&guid=5ef7e9dc-73c0-b781cc87-3397a46b1b03&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%A4%84%E7%BD%9A"
        yield Request(entrance, headers=self.headers)

    def parse(self, response):
        if re.search('eval\(function\(p,a,c,k,e,r', response.text):
            javascript_code = response.text
            dynamicUrl, wzWsQuestion, wzWsFactor = \
                re.search('dynamicurl="(.*?)".*?wzwsquestion="(.*?)".*?wzwsfactor="(.*?)"', javascript_code).groups()
            wzWsChallenge = anti_first.call('anti_first', wzWsQuestion, wzWsFactor)
            dynamicUrl = response.urljoin(dynamicUrl) + "?wzwschallenge=" + wzWsChallenge
            headers = self.headers
            headers["Cookie"] = response.headers["Set-Cookie"]
            yield Request(dynamicUrl, self.parse1, headers=headers, dont_filter=True)
        else:
            self.parse(response)

    def parse1(self, response):
        print(response.headers)
        vjkl5 = response.headers['Set-Cookie'][0].decode()
        vjkl5 = re.search()



if __name__ == "__main__":
    MySpider.cza_run_spider()
