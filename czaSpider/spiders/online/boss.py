from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "boss-job"
    parse_item = True
    clean_item = True

    url = "https://www.zhipin.com/c101200100/?query=python&page=1"

    def start_requests(self):
        import requests  # 嵌入心跳请求
        requests.get('http://47.101.42.79:8000/heartbeat/checking', params={'machine_id': 'boss_spider'})
        yield Request(self.url)

    def parse(self, response):
        jobs = data_from_xpath(response, '//div[@class="job-list"]/ul/li')
        urls = []
        items = {}
        for job in jobs:
            item = {}
            item['job_name'] = data_from_xpath(job, './/div[@class="job-title"]/text()', first=True)
            item['job_salary'] = data_from_xpath(job, './/span[@class="red"]/text()', first=True)
            item['company_name'] = data_from_xpath(job, './/h3[@class="name"]/a/text()', join=True)
            item['job_scale'] = data_from_xpath(job, './/h3[@class="name"]/following-sibling::p//text()', join=True,
                                                sep='|')
            url = data_from_xpath(job, './/h3[@class="name"]/a/@href', url=True, source=response)
            urls.append(url)
            items.setdefault(url, item)
        try:
            yield from traverse_urls(response, self, detail_urls=urls, items=items,
                                     next_page_format="page=%d",
                                     next_page_without_new_urls=True)
        except:
            pass


if __name__ == '__main__':
    MySpider.cza_run_spider()
