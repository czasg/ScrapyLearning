import logging, random

from czaSpider.czaBaseSpider import IOCO
# from sougou_code import SogouCode
from czaSpider.czaTools import *
def get_url_from_js(spider, response, url):
    if "url=" not in url or "&k=" in url:
        return url
    try:
        parseint = re.search('a=this\.href\.substr\(a\+4\+parseInt\("(\d+)"\)\+b,1\)', response.text).group(1)
        b = random.choice(range(100)) + 1
        h = url[url.index("url=") + 4 + int(parseint) + b]
        return url + "&k=" + str(b) + "&h=" + h
    except:
        spider.log("微信url加密规则发生了变化" + "".join(re.findall("<script>[\s\S]+?</script>", response.text)), level=logging.ERROR)
        raise
def redirect_to_request_callback(func):
    def wrapper(spider, response):
        if "url.replace(\"@\", \"\");" in response.text:
            url = "".join(re.findall("url\s*\+?=\s*'(.*?)';", response.text)).replace("@", "")
            spider.log("识别到js重定向", level=logging.INFO)
            yield Request(url, response.request.callback, meta=response.meta)
            return
        yield from func(spider, response)

    return wrapper

class MySpider(IOCO):
    name = "wechat1-wechat"
    url_article_search_template = "https://weixin.sogou.com/weixin?type=2&s_from=input&query={query}&ie=utf8&_sug_=n&_sug_type_=&page=1"
    url_article_advanced_search_template = "https://weixin.sogou.com/weixin?" \
                                           "usip={usip}&query={query}&ft=&tsn=3&et=&interation=&type=2&wxid={wxid}&page=1&ie=utf8"

    def start_requests(self):
        self.target = self.settings.get('target')
        if not self.target:
            raise Exception('Must Point One Target To Search!')
        yield Request(self.url_article_search_template.format(query=self.target))

    def parse(self, response):
        wxid = None
        all_s_p = data_from_xpath(response, '//div[@class="s-p"]/a')
        for s_p in all_s_p:
            if data_from_xpath(s_p, './text()', first=True) == self.target:
                wxid = data_from_xpath(s_p, './@i', first=True)
                self.log("获取到wxid: %s" % wxid, level=logging.INFO)
                break
        if wxid:
            yield Request(self.url_article_advanced_search_template.format(query=self.target, usip=self.target, wxid=wxid),
                          self.wenzhang_get_list_content)
        else:
            self.log("未获取到wxid。即检索文章列表中，无公众号【 %s 】的文章，无法进入高级检索" % self.target, level=logging.INFO)

    def wenzhang_get_list_content(self, response):
        all_txt_box = data_from_xpath(response, '//div[@class="txt-box"]')
        new = 0
        for txt_box in all_txt_box:
            from_official_account = data_from_xpath(txt_box, './div[@class="s-p"]/a/text()', first=True)
            if from_official_account != self.target:  # 文章的来源公众号不是目标公众号，过滤
                continue
            title = data_from_xpath(txt_box, './h3/a//text()', join=True)
            pubdate = datetime.datetime.fromtimestamp(int(data_from_xpath(txt_box, './div[@class="s-p"]/@t', first=True)))
            # if self.dup_filter(self.target, title, pubdate):  # 去重
            #     continue
            new += 1
            url = data_from_xpath(txt_box, './h3/a/@href', first=True)
            url = get_url_from_js(self, response, url)
            print(title, pubdate, response.urljoin(url))
            # continue
            yield Request(response.urljoin(url), self.wenzhang_detail_article, dont_filter=True, meta={'title': title})
            return
        return
        urls = len(all_txt_box)
        self.log("共%d条其中%d条未爬" % (urls, new))
        self.crawler.stats.inc_value("scanned/urls", count=urls)
        self.crawler.stats.inc_value("scanned/new_urls", count=new)

        if all_txt_box:
            yield Request(get_next_page(response.url, format='page=%d'), response.request.callback)

    @redirect_to_request_callback
    def wenzhang_detail_article(self, response):
        print(response.text)
        yield

if __name__ == "__main__":
    MySpider.cza_run_spider(s={'target': '漫画厅'})
    # MySpider.file_download(thread=5)
    # MySpider.file_reParse()
