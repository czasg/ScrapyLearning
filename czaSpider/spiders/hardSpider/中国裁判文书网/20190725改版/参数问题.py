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
        "Param": "案件类型:刑事案件,法院名称:玉林市福绵区人民法院",  # 卧槽，还真和这个有强关联
        "Index": str(page),
        "Page": "5",
        "Order": "裁判日期",
        "Direction": "desc",
        "vl5x": str(vl5x),
        "number": str(number),
        "guid": str(guid),
    }
    return formData


anti_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
}

detail_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
list_url = "http://wenshu.court.gov.cn/List/ListContent"


class MySpider(IOCO):
    name = "chinaReferee-government参数问题"
    custom_settings = {'HTTPERROR_ALLOWED_CODES': [503, 502]}  # 是不是还有一种办法，MySpider.update_settings()

    def start_requests(self):
        url = "http://wenshu.court.gov.cn/List/List"
        fromdata = {
            "sorttype": "1",
            "conditions": "searchWord 1  刑事案件 案件类型: 刑事案件"}
        yield FormRequest(url, method='GET', formdata=fromdata, headers=anti_headers)

    def parse(self, response):
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
                return
            DocID = anti_third.call('anti_third', RunEval, docId)
            save_url = detail_url + "?DocID=" + DocID
            detail_urls.append(save_url)
        print(detail_urls)


if __name__ == '__main__':
    MySpider.cza_run_spider()
