from scrapy import Selector

from scrapyProj.candy.房天下.房天下base import FangTianXiaBase, get_formData
from scrapyProj.tools import *


class MySpider(FangTianXiaBase):
    cat = "零碎任务"
    name = "房天下-租房"
    dbName = "房天下"
    collName = "租房"
    website_name = "房天下-租房"
    website_url = "https://wuhan.zu.fang.com/"

    url = 'https://wuhan.zu.fang.com/house/i31/'

    def parse(self, response):
        more_city = xpath(response, '//a[contains(text(),"更多城市")]/@href', urljoin=response)
        yield Request(more_city, self.parse1)

    def parse1(self, response):
        all_cities = response.xpath('//div[@class="outCont"]/ul/li/a')
        for city in all_cities:
            url = xpath(city, './@href', urljoin=response)
            city_name = xpath(city, './text()')
            yield Request(url, self.parse2, meta={"city_name": city_name}, dont_filter=True)

    def parse2(self, response):
        all_houses = response.xpath('//div[@class="houseList"]/dl[(.//p[@class="title"])]')
        new = 0
        for house in all_houses:
            info = re.sub('id=[^\s]+', '', str(house.extract()))  # 根据@id设置热度
            url = xpath(house, './/p[@class="title"]//a/@href', urljoin=response)
            m5 = md5(info)
            if self.source_coll.count({"m5": m5}):
                continue
            if self.source_coll.count({"URL": url}):
                # 房天下网页热度设置不一致，去重m5存在问题，加入url二次去重。unique_key不更改。
                continue
            new += 1
            house_name = jxpath(house, './/p[@class="gray6 mt12"]/a[last()]//text()')
            yield FormRequest(url=self.baidu, formdata=get_formData(house_name), method='GET',
                              callback=self.process_baidu,
                              meta={'m5': m5, 'city_name': response.meta["city_name"], 'url': url, 'source': info})
        scanned_printer(self, all_houses, new)
        if new:
            url = get_next_page(response.url, formart="/i3%d", dont_print=True)
            yield response.request.replace(url=url, meta={"city_name": response.meta["city_name"]})

    @classmethod
    def process_detail(cls, response, rec, info):
        text = response[0].text
        response = Selector(text=text)
        info[constant.TITLE] = jxpath(response, '//p[@class="title"]//text()')
        info["小区地址"] = jxpath(response, '//p[@class="gray6 mt12"]//text()')
        info["小区名字"] = jxpath(response, '//p[@class="gray6 mt12"]/a[last()]//text()')
        info["租金"] = jxpath(response, '//span[@class="price"]//text()')
        info["特征标签"] = re.sub('[\n\s]', '', jxpath(response, '//p[@class="mt12"]//text()', joiner="-"))
        info["出租规格"] = re.sub('[\n\s]', '', jxpath(response, '//p[@class="font15 mt12 bold"]//text()'))
        info["百度查询地址"] = info.pop("baidu_address")
        yield info
