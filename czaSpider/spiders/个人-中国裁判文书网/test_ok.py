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
    detail_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
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
            yield Request(dynamicUrl, self.parse1, headers=headers, meta={"headers": headers}, dont_filter=True)
        else:
            self.parse(response)

    def parse1(self, response):
        headers = response.meta["headers"]
        cookie = response.headers['Set-Cookie'].decode()
        vjkl5 = re.search('vjkl5=(.*?);', cookie).group(1)
        vl5x, number, guid = anti_second.call('anti_second', vjkl5)
        formData = {
            "Param": "上传日期:2019 - 05 - 23 TO 2019 - 05 - 24, 案件类型: 刑事案件",
            "Index": "1",
            "Page": "10",
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": str(vl5x),
            "number": str(number),
            "guid": str(guid),
        }
        yield FormRequest(self.url, self.parse2, headers=headers, formdata=formData, meta={"headers": headers})

    def parse2(self, response):
        headers = response.meta["headers"]
        content = json.loads(json.loads(response.text))
        RunEval = content[0]['RunEval']
        for i in range(1, len(content)):
            docId = content[i]['文书ID']
            DocID = anti_third.call('anti_third', RunEval, docId)
            yield FormRequest(self.detail_url, self.parse3, formdata={"DocID": DocID}, method="GET", headers=headers)
            time.sleep(3)

    def parse3(self, response):
        print(response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
