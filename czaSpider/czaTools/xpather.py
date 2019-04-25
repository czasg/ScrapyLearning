from czaSpider.czaTools.scraper import data_from_xpath


class Xpather(object):
    def __init__(self, response, xpath_rule, **kwargs):
        self.response = response
        self.xpath_rule = xpath_rule
        self.kwargs = kwargs

    @property
    def none(self):
        return data_from_xpath(self.response, self.xpath_rule)

    @property
    def first(self):
        return data_from_xpath(self.response, self.xpath_rule, first=True)

    @property
    def join(self):
        return data_from_xpath(self.response, self.xpath_rule, join=True, **self.kwargs)

    @property
    def returnList(self):
        return data_from_xpath(self.response, self.xpath_rule, returnList=True)

    @property
    def url(self):
        return data_from_xpath(self.response, self.xpath_rule, url=True, **self.kwargs)

    @property
    def urls(self):
        return data_from_xpath(self.response, self.xpath_rule, urls=True, **self.kwargs)

    @property
    def article(self):
        return data_from_xpath(self.response, self.xpath_rule, article=True, **self.kwargs)


if __name__ == "__main__":
    from scrapy import Selector

    response = Selector(text="""<div class="cza"><a href="www.baidu.com"><p>hello</p><p>cza's</p><p>world</p></div>""")
    # print(Xpather(response, '//body').first)
    # print(Xpather(response, '//body/div[@class="cza"]//text()').first)

    # print(Xpather(response, '//body//text()', sep='###').join)

    # print(Xpather(response, '//body//text()').returnList)

    # print(Xpather(response, '//body').article)
