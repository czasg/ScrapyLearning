import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "wechat1-wechat"
    url_article_search_template = "https://weixin.sogou.com/weixin?type=2&s_from=input&query={query}&ie=utf8&_sug_=n&_sug_type_=&page=1"
    url_article_advanced_search_template = "https://weixin.sogou.com/weixin?type=2&ie=utf8&query={}&tsn=0" \
                                  "&ft=&et=&interation=&wxid={wxid}&usip={usip}&page=1"
    def start_requests(self):
        target = self.settings.get('target')
        if not target:
            raise Exception('Must Point One Target To Search!')
        yield Request(self.url_article_search_template.format(query=target))

    def parse(self, response):  # 这一步完全没有反爬嘛，但是后序的反爬如何写呢，特别是验证码
        all_article = data_from_xpath(response, '//ul[@class="news-list"]/li')
        for article in all_article:
            title = data_from_xpath(article, './div[@class="txt-box"]/h3//text()', join=True)
            content = data_from_xpath(article, './div[@class="txt-box"]/p[@class="txt-info"]', article=True)
            url = data_from_xpath(article, './div[@class="txt-box"]/h3/a/@href', url=True, source=response)
            print([title, content, url])
            yield
            return



if __name__ == "__main__":
    MySpider.cza_run_spider(s={'target': '海贼王'})
    # MySpider.file_download(thread=5)
    # MySpider.file_reParse()
