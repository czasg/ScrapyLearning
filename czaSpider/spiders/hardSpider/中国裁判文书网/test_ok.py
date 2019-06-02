import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "chinaReferee-government"

    url = "http://wenshu.court.gov.cn/List/ListContent"
    detail_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
    entrance = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=3YHLPLNF" \
               "&guid=5ef7e9dc-73c0-b781cc87-3397a46b1b03&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%A4%84%E7%BD%9A"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }
    PAGE = 1

    def __init__(self):
        super(MySpider, self).__init__()
        with open('zgcpwsw1.js', encoding='utf-8') as f:
            js = f.read()
            self.anti_first = execjs.compile(js)

        with open('zgcpwsw2.js', encoding='utf-8') as f:
            js = f.read()
            self.anti_second = execjs.compile(js)

        with open('zgcpwsw3.js', encoding='utf-8') as f:
            js = f.read()
            self.anti_third = execjs.compile(js)

    def start_requests(self):
        yield Request(self.entrance, headers=self.headers, dont_filter=True)

    def parse(self, response):
        if re.search('eval\(function\(p,a,c,k,e,r', response.text):
            print("??????????hahahah, go here!!!!!!!!!!!!!")
            javascript_code = response.text
            dynamicUrl, wzWsQuestion, wzWsFactor = \
                re.search('dynamicurl="(.*?)".*?wzwsquestion="(.*?)".*?wzwsfactor="(.*?)"', javascript_code).groups()
            wzWsChallenge = self.anti_first.call('anti_first', wzWsQuestion, wzWsFactor)
            dynamicUrl = response.urljoin(dynamicUrl) + "?wzwschallenge=" + wzWsChallenge
            headers = self.headers
            headers["Cookie"] = response.headers["Set-Cookie"]
            # self.new_headers = headers
            self.headers = headers
            yield Request(dynamicUrl, self.parse1, headers=self.headers, dont_filter=True)
        else:
            print('?????????go here??????????')
            cookie = response.headers['Set-Cookie'].decode()
            vjkl5 = re.search('vjkl5=(.*?);', cookie).group(1)
            vl5x, number, guid = self.anti_second.call('anti_second', vjkl5)
            print("vl5x: ", vl5x)
            formData = {
                "Param": "全文检索:合同",
                "Index": str(self.PAGE),
                "Page": "10",
                "Order": "法院层级",
                "Direction": "asc",
                "vl5x": str(vl5x),
                "number": str(number),
                "guid": str(guid),
            }
            print("formdata: ", formData)
            yield FormRequest(self.url, self.parse2, headers=self.headers, formdata=formData, dont_filter=True)

    def parse1(self, response):
        print('????????????????')
        cookie = response.headers['Set-Cookie'].decode()
        vjkl5 = re.search('vjkl5=(.*?);', cookie).group(1)
        vl5x, number, guid = self.anti_second.call('anti_second', vjkl5)
        print("vl5x: ", vl5x)
        formData = {
            "Param": "全文检索:合同",
            "Index": str(self.PAGE),
            "Page": "10",
            "Order": "法院层级",
            "Direction": "asc",
            "vl5x": str(vl5x),
            "number": str(number),
            "guid": str(guid),
        }
        print("formdata: ", formData)
        yield FormRequest(self.url, self.parse2, headers=self.headers, formdata=formData, dont_filter=True)

    def parse2(self, response):
        content = json.loads(json.loads(response.text))
        RunEval = content[0]['RunEval']
        detail_urls = []
        print(content)
        print(RunEval)
        for i in range(1, len(content)):
            print(content[i])
            try:
                docId = content[i]['文书ID']
            except KeyError:
                print('No 文书ID')
                yield Request(self.entrance, self.parse, headers=self.headers, dont_filter=True)
                return
            DocID = self.anti_third.call('anti_third', RunEval, docId)
            save_url = self.detail_url + "?DocID=" + DocID
            detail_urls.append(save_url)
        # yield from traverse_urls(response, self,
        #                          detail_urls=detail_urls,
        #                          allow_next_page=False,
        #                          extend_callback=lambda url: Request(url, self.parse3, headers=self.headers),
        #                          request_delay=2)
        self.PAGE += 1
        print(self.PAGE)
        yield Request(self.entrance, self.parse, headers=self.headers, dont_filter=True)

    def parse3(self, response):
        yield self.process_item(url=response.url, html=response.text)

    @classmethod
    def process_detail(cls, response, document, info):
        for i in range(5000):
            info["test"] = "test"
            yield info


if __name__ == "__main__":
    # MySpider.cza_run_spider()
    # MySpider.file_download(thread=5)
    import time

    start = time.time()
    # MySpider.file_reParse()
    MySpider.test()
    print("Done!, using: %s" % str(time.time() - start))
