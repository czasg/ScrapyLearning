from czaSpider.czaBaseSpider import IOCO


class MySpider(IOCO):
    name = "downloadTest-test"

    url = "http://www.xianning.gov.cn/xxgk/zfld/wyh/"

    def parse(self, response):  # todo，终极大bug，会重复两次下载！！！！
        # print(response.url)
        yield self.process_item(url=response.url)
        yield self.process_item(html=[response.url, "hello, world1"])
        yield self.process_item(html="hello, world2")
        yield self.process_item(html="hello, world3")
        yield self.process_item(html="hello, world4")
        yield self.process_item(html="hello, world5")
        yield self.process_item(html="hello, world6")
        yield self.process_item(html="hello, world7")
        yield self.process_item(html="hello, world8")
        yield self.process_item(html="hello, world9")

    @classmethod
    def process_detail(cls, response, document, info):
        info['test'] = '123'
        info['test1'] = '123'
        yield info


if __name__ == "__main__":
    # MySpider.cza_run_spider()
    MySpider.file_download(delay=2)
    # MySpider.file_parse()
    # MySpider.file_reParse()
    # MySpider.mongodb2csv(source=True)
