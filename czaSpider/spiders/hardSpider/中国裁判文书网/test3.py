import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

url = "http://wenshu.court.gov.cn/list/list/?sorttype=1"
list_url = "http://wenshu.court.gov.cn/List/ListContent"
detail_url = "http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx"
key_url = "http://wenshu.court.gov.cn/List/TreeContent"

anti_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"}

keywords = ['诈骗', '盗窃', '造假', '纠纷', '受贿', '行贿', '聚众斗殴', '出逃', '滥用', '集资', '操纵', '虚假', '泄露',
            '洗钱', '偷税', '抗税', '漏税', '非法', '银行', '券商', '保险', '票据', '合同', '贷款', '货币', '赔偿',
            '借贷', '诉讼', '经营', '信用', '专利', '销售', '内幕', '职务侵占', '走私']
provinces = ['山东', '江苏', '上海', '浙江', '安徽', '福建', '江西', '广东', '广西', '海南',
             '河南', '湖南', '湖北', '北京', '天津', '河北', '山西', '宁夏', '青海', '内蒙古',
             '陕西', '甘肃', '新疆', '四川', '贵州', '云南', '重庆', '西藏', '辽宁', '吉林', '黑龙江']

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


def refresh_formData(key, vl5x, number, guid):
    formData = {
        "Param": key,
        "Index": "1",
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": str(vl5x),
        "number": str(number),
        "guid": str(guid),
    }
    return formData


class AntiJS:
    def __init__(self, spider, response):
        print("enter AntiJS...")
        self.spider = spider
        self.response = response
        self.callback = response.request.callback

    def anti_first(self):
        javascript_code = self.response.text
        dynamicUrl, wzWsQuestion, wzWsFactor = \
            re.search('dynamicurl="(.*?)".*?wzwsquestion="(.*?)".*?wzwsfactor="(.*?)"',
                      javascript_code).groups()
        wzWsChallenge = anti_first.call('anti_first', wzWsQuestion, wzWsFactor)
        dynamicUrl = self.response.urljoin(dynamicUrl) + "?wzwschallenge=" + wzWsChallenge
        yield self.response.request.replace(url=dynamicUrl, dont_filter=True)

    def anti_remind_key(self):
        print("Enter Anti remind_key")
        yield Request(url, self.spider.parse, headers=anti_headers, dont_filter=True)

    @classmethod
    def auto(cls, func):
        def wrapper(spider, response):
            if re.search('eval\(function\(p,a,c,k,e,r', response.text):
                anti = cls(spider, response)
                yield from anti.anti_first()
                print("Finished AntiJS...")
                return
            elif re.match("\"remind key\"", response.text):
                anti = cls(spider, response)
                yield from anti.anti_remind_key()
                return
            print('enter No antiJS...')
            yield from func(spider, response)

        return wrapper


class MySpider(IOCO):
    name = "chinaReferee3-government"
    key = "全文检索:合同"

    def start_requests(self):
        yield Request(url, headers=anti_headers, dont_filter=True)

    @AntiJS.auto
    def parse(self, response):
        cookie = response.headers['Set-Cookie'].decode()
        vjkl5 = re.search('vjkl5=(.*?);', cookie).group(1)
        vl5x, number, guid = anti_second.call('anti_second', vjkl5)
        self.formData = refresh_formData(self.key, vl5x, number, guid)
        yield FormRequest(list_url, self.parse2, headers=anti_headers, formdata=self.formData,
                          dont_filter=True)
        # key_params = {
        #     "Param": self.key,
        #     "vl5x": str(vl5x),
        #     "number": str(number),
        #     "guid": str(guid),
        # }
        # yield FormRequest(key_url, self.key_parse, headers=anti_headers, formdata=key_params,
        #                   dont_filter=True)

    @AntiJS.auto
    def parse2(self, response):
        content = json.loads(json.loads(response.text))
        RunEval = content[0]['RunEval']
        new = 0
        for i in range(1, len(content)):
            try:
                docId = content[i]['文书ID']
            except KeyError:
                print('No 文书ID, request again!')
                yield Request(url, self.parse, headers=anti_headers, dont_filter=True)
                return
            DocID = anti_third.call('anti_third', RunEval, docId)
            save_url = detail_url + "?DocID=" + DocID
            if self.mongo.source.count(url=save_url).docs:
                continue
            new += 1
            yield Request(save_url, self.parse3, headers=anti_headers)
        print("共%d条其中%d条未爬" % (len(content) - 1, new))
        if new:
            self.formData = json.loads(get_next_page(json_data=self.formData, format="Index=%d"))
            yield FormRequest(list_url, self.parse2, headers=anti_headers, formdata=self.formData,
                              dont_filter=True)

    def parse3(self, response):
        yield self.process_item(url=response.url, html=response.text)

    @AntiJS.auto
    def key_parse(self, response):
        if response.text:
            print(response.text)
            key_data = json.loads(json.loads(response.text))
            Keys = [{data["Key"]: [child["Key"] for child in data["Child"] if child["Key"]]} for data in key_data]
            print(Keys)  # todo, maybe push those keys to redis database
        else:
            print("Get No Key: %s" % response.text)
        yield

    @classmethod
    def process_detail(cls, response, document, info):
        info["text"] = xpather(response, '.').article
        info["url"] = response.url
        yield info


if __name__ == "__main__":
    MySpider.cza_run_spider()
    # MySpider.file_download()
    # MySpider.file_reParse(thread=3)
    # MySpider.file_parse(thread=3)
