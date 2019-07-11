from scrapy import Selector

from scrapyProj.candy.房天下.房天下base import FangTianXiaBase, get_formData
from scrapyProj.tools import *


class MySpider(FangTianXiaBase):
    cat = "零碎任务"
    name = "房天下-写字楼"
    dbName = "房天下"
    collName = "写字楼"
    website_name = "房天下-写字楼"
    website_url = "https://wuhan.office.fang.com/"

    url = 'https://wuhan.office.fang.com/zu/house/i31/'

    def parse(self, response):
        all_cities = response.xpath('//div[@class="city20141104nr"][1]/a[@href]')
        for city in all_cities:
            url = xpath(city, './@href', urljoin=response)
            city_name = xpath(city, './text()')
            yield Request(url, self.parse1, meta={"city_name": city_name, "url": url}, dont_filter=True)

    def parse1(self, response):
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
            house_name = xpath(house, './/p[@class="gray6 mt15"]/a/@title')
            yield FormRequest(url=self.baidu, formdata=get_formData(house_name), method='GET',
                              callback=self.process_baidu,
                              meta={'m5': m5, 'city_name': response.meta["city_name"], 'url': url, 'source': info})
        scanned_printer(self, all_houses, new)
        if new:
            url = get_next_page(response.url, formart="/i3%d", dont_print=True)
            yield response.request.replace(url=url, meta={"city_name": response.meta["city_name"], "url": url})

    @classmethod
    def process_detail(cls, response, rec, info):
        text = response[0].text
        response = Selector(text=text)
        info[constant.TITLE] = xpath(response, '//p[@class="title"]//a/@title')
        info["小区名字"] = xpath(response, '//p[@class="gray6 mt15"]/a/@title')
        info["图片数量"] = xpath(response, '//span[@class="iconImg"]/text()')
        info["建筑面积"] = jxpath(response, '//div[@class="area area2 alignR"]/text()')
        info["每平米月租金"] = re.sub('[\s\n]', '', jxpath(response, '//p[@class="mt5 alignR"]//text()'))
        info["月租金"] = re.sub('[\s\n]', '', jxpath(response, '//p[@class="danjia alignR mt5 gray6"]//text()'))
        info["小区地址"] = jxpath(response, '//p[@class="gray6 mt15"]/span/@title', joiner="-")
        info["代表人"] = xpath(response, '//a[@class="marr7"]/text()')

        content = get_dict_from_sentence(jxpath(response, '//p[@class="gray6 mt10"][1]/text()'), spliter="\r\n")
        if content:
            info.update(content)
        info["百度查询地址"] = info.pop("baidu_address")
        yield info
