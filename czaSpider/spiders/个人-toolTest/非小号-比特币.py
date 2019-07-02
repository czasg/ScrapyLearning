from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = 'btc-feiXiaoHao'
    parse_item = True
    clean_item = True

    url = "https://dncapi.bqiapp.com/api/coin/web-coinrank?page=1&type=-1&pagesize=100&webp=1"

    def parse(self, response):
        json_data = json.loads(response.text)
        new = 0
        for data in json_data['data']:
            fullname = data['fullname']
            current_price = data['current_price']
            if fullname in self.filters:
                continue
            self.filters.append(fullname)
            new += 1
            yield self.process_item(fullname=fullname, current_price=current_price)
        if new:
            yield Request(get_next_page(response.url, 'page=%d'), response.request.callback)

if __name__ == '__main__':
    # MySpider.cza_run_spider()
    MySpider.mongodb2json(source=True, dropColumn='_id')