from scrapy import Selector

from scrapyProj.candy.房天下.房天下base import FangTianXiaBase, get_formData
from scrapyProj.tools import *


class MySpider(FangTianXiaBase):
    cat = "零碎任务"
    name = "房天下-新房"
    dbName = "房天下"
    collName = "新房"
    website_name = "房天下-新房"
    website_url = "https://wuhan.newhouse.fang.com/house/s/"

    url = 'https://wuhan.newhouse.fang.com/house/s/b91/'

    def parse(self, response):
        all_cities = response.xpath('//div[@class="city20141104nr"][position()>1]/a[@href]')
        for city in all_cities:
            url = xpath(city, './@href', urljoin=response)
            city_name = xpath(city, './text()')
            yield Request(url, self.parse1, meta={"city_name": city_name}, dont_filter=True)

    def parse1(self, response):
        all_houses = response.xpath('//div[@id="newhouse_loupai_list"]/ul/li[(.//div[@class="nlcd_name"])]')
        new = 0
        for house in all_houses:
            info = re.sub('id=[^\s]+', '', str(house.extract()))  # 根据@id进行设置热度，删除热度部分
            url = xpath(house, './/div[@class="nlcd_name"]//a/@href', urljoin=response)
            m5 = md5(info)
            if self.source_coll.count({"m5": m5}):
                continue
            if self.source_coll.count({"URL": url}):
                # 房天下网页热度设置不一致，去重m5存在问题，加入url二次去重。unique_key不更改。
                continue
            new += 1
            house_name = jxpath(house, './/div[@class="nlcd_name"]//text()')
            yield FormRequest(url=self.baidu, formdata=get_formData(house_name), method='GET',
                              callback=self.process_baidu,
                              meta={'m5': m5, 'city_name': response.meta["city_name"], 'url': url, 'source': info})
        scanned_printer(self, all_houses, new)
        if new:
            url = get_next_page(response.url, formart="/b9%d", dont_print=True)
            yield response.request.replace(url=url, meta={"city_name": response.meta["city_name"]})

    @classmethod
    def process_detail(cls, response, rec, info):
        text = response[0].text
        response = Selector(text=text)
        info["小区名字"] = jxpath(response, '//div[@class="nlcd_name"]//text()')
        info["房价"] = re.sub('[广告\s\n]', '', jxpath(response, '//div[@class="nhouse_price"]//text()'))
        info["特征标签"] = re.sub('[\n\s]', '', jxpath(response, '//div[@class="fangyuan"]//text()', joiner="-"))
        info["小区地址"] = re.sub('[\n\s]', '', jxpath(response, '//div[@class="address"]//a/@title'))
        info["规模"] = re.sub('[\n\s]', '', jxpath(response, '//div[@class="house_type clearfix"]//text()'))
        info["图片数量"] = jxpath(response, '//div[@class="infbg"]//text()')
        info["评论数量"] = rea.search('(\d+)', jxpath(response, '//span[@class="value_num"]/text()')).group(1)

        starts = re.search('allstar = (.*?);.*?halfstar = (.*?);', text, flags=re.S)
        if starts:
            allstar, halfstar = starts.groups()
            info["星级指数"] = str(int(allstar) + int(halfstar) * 0.5) + "颗星"
        info["百度查询地址"] = info.pop("baidu_address")
        yield info
