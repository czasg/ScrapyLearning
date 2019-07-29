import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

try:
    with open('zgcpwsw2.js', encoding='utf-8') as f:
        js = f.read()
        anti_second = execjs.compile(js)

    with open('zgcpwsw3.js', encoding='utf-8') as f:
        js = f.read()
        anti_third = execjs.compile(js)
except:
    pass

PAGE = 1


def refresh_formData(page, vl5x, number, guid):
    formData = {
        # "Param": "全文检索:合同",
        "Param": "案件类型:行政案件",  # 卧槽，还真和这个有强关联
        "Index": str(page),
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": str(vl5x),
        "number": str(number),
        "guid": str(guid),
    }
    return formData


# entrance = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6"
entrance = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E8%A1%8C%E6%94%BF%E6%A1%88%E4%BB%B6"
anti_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}
detail_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
list_url = "http://wenshu.court.gov.cn/List/ListContent"


class MySpider(IOCO):
    name = "chinaReferee20190725-government"
    # 3ba71c93ffd53c08013f1870cdd5c300eb0d5f62  这是网页计算出来的
    # ab42fa0cc1c0b63e0eb0f63d
    # ab42fa0cc1c0b63e0eb0f63d  - 一模一样，书名加密算法规则没有变

    # 31a10293ffe33c46016418d1bcab02e07308a06b  这是我计算出来的
    # d0d8ed5b6d0bc6def563ddbe
    custom_settings = {'HTTPERROR_ALLOWED_CODES': [503, 502]}

    def start_requests(self):
        yield Request(entrance, headers=anti_headers, dont_filter=True)

    def parse(self, response):
        print(response.request.cookies)
        print(response.headers)
        vjkl5 = re.search("vjkl5=(.*?);", str(response.headers)).group(1)
        print('获取到了vjkl5:', vjkl5)
        vl5x, guid, number = anti_second.call('anti_second', vjkl5)
        number = 'wens'
        formData = refresh_formData(PAGE, vl5x, number, guid)
        print(formData)
        global anti_headers
        anti_headers['Cookie'] = response.headers["Set-Cookie"].decode()
        yield FormRequest(list_url, self.parse2, headers=anti_headers, formdata=formData, dont_filter=True)

    def parse2(self, response):
        print(response.text)
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
        print(detail_urls)


if __name__ == '__main__':
    MySpider.cza_run_spider()
    # vjkl5 = '31a10293ffe33c46016418d1bcab02e07308a06b'
    # vjkl5 = '3ba71c93ffd53c08013f1870cdd5c300eb0d5f62'
    # vl5x, guid, number = anti_second.call('anti_second', vjkl5)
    # print(vl5x)


"""
Param: 案件类型:刑事案件
Index: 1
Page: 10
Order: 法院层级
Direction: asc
vl5x: 939c6dbe5a152c4546905879
number: wens
guid: 7ef6725a-cae9-6a5c706a-4ee9a3b53beb

Param: 案件类型:民事案件
Index: 1
Page: 10
Order: 法院层级
Direction: asc
vl5x: 7c409f284a6e8e0f5c897140
number: wens
guid: 7b253255-1169-da631ccb-c1a114b1eee4

不加参数居然不会有数据???? - 这是一个方向，明天可以考虑考虑
案件类型:刑事案件、民事案件、行政案件、赔偿案件、执行案件
"""
