from scrapy import Selector

from scrapyProj.candy.房天下.房天下base import FangTianXiaBase, get_formData
from scrapyProj.tools import *


class MySpider(FangTianXiaBase):
    cat = "零碎任务"
    name = "房天下-商铺"
    dbName = "房天下"
    collName = "商铺"
    website_name = "房天下-商铺"
    website_url = "https://wuhan.shop.fang.com/"

    url = 'https://wuhan.shop.fang.com/shou/house/i31/'

    def parse(self, response):
        all_cities = response.xpath('//div[@class="city20141104nr"][1]/a[@href]')
        for city in all_cities:
            url = xpath(city, './@href', urljoin=response)
            city_name = xpath(city, './text()')
            yield Request(url, self.parse1, meta={"city_name": city_name, "url": url}, dont_filter=True)

    def parse1(self, response):
        all_houses = response.xpath('//div[@class="shop_list"]/dl[(.//span[@class="tit_shop"])]')
        new = 0
        for house in all_houses:
            info = re.sub('id=[^\s]+', '', str(house.extract()))  # 根据@id设置热度
            url = xpath(house, './/h4[@class="clearfix"]//a/@href', urljoin=response)
            m5 = md5(info)
            if self.source_coll.count({"m5": m5}):
                continue
            if self.source_coll.count({"URL": url}):
                # 房天下网页热度设置不一致，去重m5存在问题，加入url二次去重。unique_key不更改。
                continue
            new += 1
            house_name = xpath(house, './/p[@class="add_shop"]/a/@title')
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
        info[constant.TITLE] = xpath(response, '//h4[@class="clearfix"]//a/@title')
        info["小区名字"] = xpath(response, '//p[@class="add_shop"]/a/@title')
        info["建筑面积"] = jxpath(response, '//span[@class="color3"]//text()')
        info["每平米售价"] = re.sub('[\s\n]', '', jxpath(response, '//dd[@class="price_right"]/span[2]//text()'))
        info["总价"] = re.sub('[\s\n]', '', jxpath(response, '//dd[@class="price_right"]/span[1]//text()'))
        info["小区地址"] = jxpath(response, '//p[@class="add_shop"]/span/@title', joiner="-")
        info["代表人"] = jxpath(response, '//p[@class="people_name"]//text()')

        content = get_dict_from_sentence(jxpath(response, '//p[@class="tel_shop"]/text()', joiner="\r\n"),
                                         spliter="\r\n")
        if content:
            info.update(content)
        info["百度查询地址"] = info.pop("baidu_address")
        yield info
