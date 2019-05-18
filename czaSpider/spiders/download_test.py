from czaSpider.czaBaseSpider import IOCO


class MySpider(IOCO):
    name = "downloadTest-test"

    url = "http://www.xianning.gov.cn/xxgk/zfld/wyh/"

    def parse(self, response):  # todo，终极大bug，会重复两次下载！！！！
        yield self.process_item(url=response.url)
        # print(response.url)


if __name__ == "__main__":
    # MySpider.cza_run_spider()
    MySpider.file_download()