from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "fangtx-zufang"
    parse_item = True
    clean_item = True

    url = 'https://wuhan.zu.fang.com/house/i31/'

    def start_requests(self):
        import requests  # 嵌入心跳请求
        requests.get('http://47.101.42.79:8000/heartbeat/checking', params={'machine_id': 'fangtx_spider'})
        yield Request(self.url)

    def parse(self, response):
        houses = data_from_xpath(response, '//div[@class="houseList"]/dl[(.//p[@class="title"])]')
        urls = []
        items = {}
        for house in houses:
            item = {}
            item["小区地址"] = data_from_xpath(house, './/p[@class="gray6 mt12"]//text()', join=True)
            item["小区名字"] = data_from_xpath(house, './/p[@class="gray6 mt12"]/a[last()]//text()', join=True)
            item["租金"] = data_from_xpath(house, './/span[@class="price"]//text()', join=True)
            item["特征标签"] = re.sub('\s', '', data_from_xpath(house, './/p[@class="mt12"]//text()', join=True, sep="|"))
            item["出租规格"] = re.sub('\s', '',
                                  data_from_xpath(house, './/p[@class="font15 mt12 bold"]//text()', join=True))
            url = data_from_xpath(house, './/p[@class="title"]//a/@href', url=True, source=response)
            urls.append(url)
            items.setdefault(url, item)
        yield from traverse_urls(response, self, detail_urls=urls,items=items, next_page_format="/i3%d")


if __name__ == '__main__':
    MySpider.cza_run_spider()
