import requests

from queue import Queue
from scrapy.http import TextResponse

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

mq = Queue()


def get_module():
    current_path = os.path.abspath(__file__)
    return re.search('(czaSpider.*)\.py', current_path).group(1).replace(os.sep, '.')


class ProxyMiddleware:
    def process_response(self, request, response, spider):
        print('###################', response.url)
        if 'zpAntispam' in response.url:
            while True:
                print('获取代理中....')
                proxy = mq.get()
                if not proxy:
                    print('代理已使用完')
                    return response
                try:
                    proxies = {
                        'http': 'http://' + proxy,
                    }
                    r = requests.get("https://www.zhipin.com/c101200100/?query=python&page=1",
                                     proxies=proxies, timeout=1,
                                     headers={
                                         'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"})
                    if '您暂时无法继续访问' in r.text:
                        print('IP被封了，%s' % proxy)
                        continue
                    else:
                        return TextResponse(url=r.url, body=r.content, encoding='utf-8')
                except requests.exceptions.ProxyError:
                    print('%s直接代理失效' % proxy)
                    continue
                except requests.exceptions.ReadTimeout:
                    print('%s请求超时，判定失效')
                    continue
        return response


class MySpider(IOCO):
    name = "world-test111"
    parse_item = True
    clean_item = True

    url = "https://www.zhipin.com/c101200100/?query=python&page=1"
    custom_settings = {"DOWNLOADER_MIDDLEWARES": {get_module() + '.ProxyMiddleware': 100},
                       "DOWNLOAD_TIMEOUT": 20}

    def start_requests(self):
        proxy = 'https://www.xicidaili.com/nn/'
        yield Request(proxy, self.parse0)
        import requests  # 嵌入心跳请求
        requests.get('http://47.101.42.79:8000/heartbeat/checking', params={'machine_id': 'boss_spider'})

    def parse0(self, response):
        trs = data_from_xpath(response, '//table[@id="ip_list"]//tr')[1:]
        for tr in trs:
            ip = data_from_xpath(tr, './td[2]/text()', first=True)
            socket = data_from_xpath(tr, './td[3]/text()', first=True)
            if not re.match('\d+\.\d+\.\d+\.\d+', ip):
                continue
            proxy = ip + ':' + socket
            mq.put(proxy)
        yield Request(self.url, self.parse)

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
    # MySpider.cza_run_spider()
    proxies = {'http':'http://47.101.42.79:80'}
    r = requests.get("https://www.zhipin.com/c101200100/?query=python&page=1",
                     proxies=proxies, timeout=3,
                     headers={'User-Agent': "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3"})
    print(r.url)
    print(r.text)
