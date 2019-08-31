from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "ziru-housePrice-废弃"
    parse_item = True
    clean_item = True

    url = "http://wh.ziroom.com/z/nl/z3.html"

    def parse(self, response):
        city = data_from_xpath(response, '//span[@id="curCityName"]/text()', first=True)
        places = data_from_xpath(response, '//dl[@class="clearfix zIndex6"]'
                                           '/dd/ul/li/div/span[position()>1]')
        for place in places:
            area_place = data_from_xpath(place, './../preceding-sibling::span/a/text()', first=True)
            son_place = data_from_xpath(place, './a/text()', first=True)
            house_place = "-".join((city, area_place, son_place))

            url = data_from_xpath(place, './a/@href', url=True, source=response)
            yield from traverse_urls(response, self, detail_urls=url,
                                     extend_callback= \
                                         lambda url: Request(url, self.process, meta={"house_place": house_place}))

    def process(self, response):
        item = {}
        house_place = response.meta["house_place"]
        item.setdefault("house_place", house_place)
        try:
            img, price_list = re.search('"image":"(.*?)".+offset":(\[.*?\])};', response.text).groups()
        except AttributeError:
            return
        price_list = eval(price_list)

        price_template = img2num_from_url(response.urljoin(img))

        houses = data_from_xpath(response, '//div[@class="t_shuaichoose_order"]'
                                           '/following-sibling::ul[@id="houseList"]/li')
        items = {}
        urls = []
        item["house_place"] = house_place
        for index, house in enumerate(houses):
            _item = item.copy()
            price = [price_template[i] for i in price_list[index]]
            _item["house_price"] = int("".join([str(v) for v in price]))

            _item["house_name"] = data_from_xpath(house, './/a[@class="t1"]/text()', first=True)

            _item["house_area"], \
            _item["house_floor"], \
            _item["house_scale"], \
            _item["distance_from_subway"] = \
                data_from_xpath(house, './/div[@class="detail"]/p/span/text()', returnList=True)

            url = data_from_xpath(house, './/a[@class="t1"]/@href', url=True, source=response)
            urls.append(url)
            items.setdefault(url, _item)
        yield from traverse_urls(response, self, detail_urls=urls, meta=response.meta,
                                 items=items, next_page_format="p=%d",
                                 check_current_page="?p=1")


if __name__ == '__main__':
    MySpider.cza_run_spider()
