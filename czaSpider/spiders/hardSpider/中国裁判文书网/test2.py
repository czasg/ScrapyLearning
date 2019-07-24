import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

list_url = "http://wenshu.court.gov.cn/List/ListContent"

detail_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"

# entrance = "http://wenshu.court.gov.cn/list/list/?sorttype=1&number=3YHLPLNF" \
#            "&guid=5ef7e9dc-73c0-b781cc87-3397a46b1b03&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%A4%84%E7%BD%9A"
# entrance = "http://wenshu.court.gov.cn/list/list/?sorttype=1"
entrance = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
anti_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

PAGE = 1

try:
    with open('zgcpwsw1.js', encoding='utf-8') as f:
        js = f.read()
        anti_first = execjs.compile(js)

    with open('zgcpwsw2.js', encoding='utf-8') as f:
        js = f.read()
        anti_second = execjs.compile(js)

    with open('zgcpwsw3.js', encoding='utf-8') as f:
        js = f.read()
        anti_third = execjs.compile(js)
except:
    pass


def refresh_formData(page, vl5x, number, guid):
    formData = {
        "Param": "全文检索:合同",
        "Index": str(page),
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": str(vl5x),
        "number": str(number),
        "guid": str(guid),
    }
    return formData


class AntiJS:
    def __init__(self, response):
        self.response = response
        self.callback = response.request.callback

    def anti_first(self):
        print("enter AntiJS...")
        javascript_code = self.response.text
        # dynamicUrl, wzWsQuestion, wzWsFactor = \
        #     re.search('dynamicurl="(.*?)".*?wzwsquestion="(.*?)".*?wzwsfactor="(.*?)"',
        #               javascript_code).groups()
        dynamicUrl, wzWsQuestion, wzWsFactor = \
            re.search('dynamicurl\|(.*?)\|.*?wzwsquestion\|(.*?)\|.*?wzwsfactor\|(.*?)\|',
                      javascript_code).groups()
        wzWsChallenge = anti_first.call('anti_first', wzWsQuestion, wzWsFactor)
        dynamicUrl = self.response.urljoin(dynamicUrl) + "?wzwschallenge=" + wzWsChallenge
        global anti_headers
        anti_headers["Cookie"] = self.response.headers["Set-Cookie"]
        yield Request(dynamicUrl, self.callback, headers=anti_headers, dont_filter=True)

    @classmethod
    def auto(cls, func):
        def wrapper(spider, response):
            if re.search('eval\(function\(p,a,c,k,e,r', response.text):
                anti = cls(response)
                yield from anti.anti_first()
                print("Finished AntiJS...")
                return
            print(response.text)
            yield from func(spider, response)

        return wrapper


class MySpider(IOCO):
    name = "chinaReferee2-government"

    def start_requests(self):
        yield Request(entrance, headers=anti_headers, dont_filter=True)

    @AntiJS.auto
    def parse(self, response):
        print('enter No antiJS...')
        cookie = response.headers['Set-Cookie'].decode()
        vjkl5 = re.search('vjkl5=(.*?);', cookie).group(1)
        # vl5x, number, guid = anti_second.call('anti_second', vjkl5)  # todo,
        vl5x, guid, number = anti_second.call('anti_second', vjkl5)
        formData = refresh_formData(PAGE, vl5x, number, guid)
        print(formData)
        yield FormRequest(list_url, self.parse2, headers=anti_headers, formdata=formData, dont_filter=True)

    @AntiJS.auto
    def parse2(self, response):
        print(response.text)
        # return
        content = json.loads(json.loads(response.text))
        RunEval = content[0]['RunEval']
        detail_urls = []
        for i in range(1, len(content)):
            print(content[i])
            try:
                docId = content[i]['文书ID']
            except KeyError:
                print('No 文书ID, request again!')
                yield Request(entrance, self.parse, headers=anti_headers, dont_filter=True)
                return
            DocID = anti_third.call('anti_third', RunEval, docId)
            save_url = detail_url + "?DocID=" + DocID
            detail_urls.append(save_url)
        yield from traverse_urls(response, self,
                                 detail_urls=detail_urls,
                                 allow_next_page=False,
                                 extend_callback=lambda url: Request(url, self.parse3, headers=anti_headers),
                                 request_delay=2)
        global PAGE
        PAGE += 1
        yield Request(entrance, self.parse, headers=anti_headers, dont_filter=True)

    def parse3(self, response):
        yield self.process_item(url=response.url, html=response.text)


if __name__ == "__main__":
    MySpider.cza_run_spider()
    # MySpider.file_download(thread=5)
    # MySpider.file_reParse()
