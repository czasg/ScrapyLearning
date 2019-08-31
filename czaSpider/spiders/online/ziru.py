from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

price_list = [0, 21, 42, 64, 85, 107, 128, 149, 171, 192]


class MySpider(IOCO):
    name = "ziru-housePrice"
    parse_item = True

    url = "http://wh.ziroom.com/z/z0-p1/"

    def start_requests(self):
        import requests  # 嵌入心跳请求
        requests.get('http://47.101.42.79:8000/heartbeat/checking', params={'machine_id': 'ziru_spider'})
        yield Request(self.url)

    def parse(self, response):
        city = data_from_xpath(response, '//dt[@class="Z_city_name"]/text()', first=True)
        places = data_from_xpath(response, '//a[text()="区域"]/following-sibling::div//a')
        for place in places:
            area_place = data_from_xpath(place, './text()', first=True)
            house_place = "-".join((city, area_place))
            url = data_from_xpath(place, './@href', url=True, source=response)
            yield from traverse_urls(response, self, detail_urls=url,
                                     extend_callback= \
                                         lambda url: Request(url, self.process, meta={"house_place": house_place}))

    def process(self, response):
        item = {}
        house_place = response.meta["house_place"]
        item.setdefault("house_place", house_place)

        houses = data_from_xpath(response, '//div[@class="Z_list"]/div[@class="Z_list-box"]'
                                           '/div[@class="item"][(./div[@class="info-box"])]')

        img_url = re.search('url\((.*?)\)', response.text).group(1)
        house_price_list = img2num_from_url(response.urljoin(img_url))
        # print(house_price_list, response.urljoin(img_url))

        items = {}
        urls = []
        for house in houses:
            _item = item.copy()
            _item["house_name"] = data_from_xpath(house, './div[@class="info-box"]//h5/a/text()', first=True)
            _item["house_area"], \
            _item["house_floor"] = data_from_xpath(house, './div[@class="info-box"]/div[@class="desc"]/div[1]'
                                                          '/text()', first=True).split('|', maxsplit=1)
            _item["distance_from_subway"] = data_from_xpath(house,
                                                            './div[@class="info-box"]/div[@class="desc"]/div[@class="location"]/text()',
                                                            join=True)

            prices_style = data_from_xpath(house,
                                           './div[@class="info-box"]/div[@class="price"]/span[@class="num"]/@style',
                                           returnList=True)
            price = []
            for price_style in prices_style:
                position_num = re.search('position:\s*-(.*?)px', price_style).group(1)
                price.append(house_price_list[price_list.index(int(float(position_num)))])
            _item["house_price"] = int(''.join(map(lambda x: str(x), price)))

            url = data_from_xpath(house, './div[@class="info-box"]//h5/a/@href', url=True, source=response)
            urls.append(url)
            items.setdefault(url, _item)

        # yield from traverse_urls(response, self, detail_urls=urls, meta=response.meta,
        #                          items=items, allow_next_page=False, next_page_by_xpath=True,
        #                          next_page_xpath='//a[text()="下一页"]/@href')


if __name__ == '__main__':
    MySpider.cza_run_spider()
