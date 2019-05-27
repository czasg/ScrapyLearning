from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "amazon-goods"
    parse_item = True

    url = "https://www.amazon.cn/s?" \
          "k=men+wallet" \
          "&page=1" \
          "&__mk_zh_CN=%E4%BA%9A%E9%A9%AC%E9%80%8A%E7%BD%91%E7%AB%99" \
          "&qid=1558163816"

    def parse(self, response):
        print('hello')
        # all_goods = data_from_xpath(response,
        #                             '//div[@class="sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item sg-col-4-of-28 sg-col-4-of-16 sg-col sg-col-4-of-20 sg-col-4-of-32"]')
        # for goods in all_goods:
        #     name = data_from_xpath(goods,
        #                            './/span[@class="a-size-base-plus a-color-base a-text-normal"]/text()',
        #                            first=True)
        #     price = data_from_xpath(goods,
        #                             './/span[@class="a-price-whole"]/text()',
        #                             returnList=True)
        #     yield self.process_item(url=response.url, goods_name=name, goods_price='-'.join(price))
        # if all_goods:
        #     print('获取%d, 跳转下一页' % len(all_goods))
        #     yield Request(get_next_page(response.url, 'page=%d'), response.request.callback)





if __name__ == "__main__":
    MySpider.cza_run_spider()
    # MySpider.mongodb2csv(source=True)
