import re
import html

from scrapy import Request

from czaSpider.czaTools.url_func import get_next_page
from czaSpider.czaTools.constant import post_dict
from czaSpider.czaTools.data_manipulation import arrayJoin


def traverse_urls(response, spider, xpath_rule=None, next_page_format=None, next_page_without_new_urls=False,
                  allow_next_page=True, meta=None, callback=None, extend_callback=None, filter_diplicate=True,
                  **kwargs):
    """
    遍历url，封装了翻页逻辑
    :param response:
    :param spider:
    :param xpath_rule: xpath规则
    :param next_page_format: 翻页的样式，如"index_%d"、"p=%d"。有去重逻辑，无新url则不会翻页
    :param next_page_without_new_urls: 当不存在新url时，可以翻页
    :param allow_next_page: 允许翻页
    :param meta:
    :param callback: 回调函数
    :param extend_callback: 其他的回调，可以指定form请求
    :param kwargs:
    :return:
    """
    detail_urls = kwargs.get("detail_urls", None)
    urls = detail_urls if detail_urls else data_from_xpath(response, xpath_rule, urls=True)
    urls = urls if isinstance(urls, list) else [urls]
    url_pipe = kwargs.get("url_pipe", None)
    urls = [url_pipe(url) for url in urls] if url_pipe else urls
    for pipe in kwargs.get("url_pipes", []):
        urls = [pipe(url) for url in urls]

    # 去重
    if filter_diplicate:
        new_urls = [url for url in urls if not spider.collection.count({"url": url})]
        _urls = new_urls
        print("共%d条其中%d条未爬" % (len(urls), len(new_urls)))
    else:
        new_urls = []
        _urls = urls
        print("未开启去重模块，默认为获取到的所有urls")
    for url in _urls:
        if not url:
            continue
        if extend_callback:
            yield extend_callback(url)
        elif callback:
            yield Request(url, callback, meta=meta)
        else:
            item = kwargs.get("items", {})
            if item:
                item = item.get(url, {})
            if isinstance(item, dict):
                item.setdefault("url", url)
                yield spider.process_item(**item)
            else:
                raise Exception("parameter items must be an dict")

    if allow_next_page and new_urls or (urls and next_page_without_new_urls):
        if response.request.method == "GET":
            yield Request(get_next_page(response.url, next_page_format, **kwargs), response.request.callback, meta=meta)
        else:
            yield Request(response.url, response.request.callback,
                          body=get_next_page(response.request.body.decode(), next_page_format, **kwargs).encode(),
                          **post_dict)


def data_from_xpath(response, xpath_rule, first=False, join=False, returnList=False,
                    url=False, urls=False, article=False, **kwargs):
    """
    从xpath中获取数据，（封装extract()、extract_first()、response.urljoin()）
    :param response: scrapy的response数据结构 or Select数据结构，若为后者，请附带参数"source=response"指定源
    :param xpath_rule: xpath获取规则
    :param first: 请参考学长你自己写的xpath()功能
    :param join: 请参考学长你自己写的jxpath()功能
    :param returnList: extract()返回列表，参考response.xpath(xpath_rule).extract()
    :param is_url: 获取xpath中单个url并返回response.urljoin()清洗结果，
                    参考response.urljoin(response.xpath(xpath_rule).extract_first())
    :param is_urls: 获取xpath中多个urls，并返回response.urljoin()清洗结果，
                    参考[response.urljoin(url) for url in urls]，其中urls为extract()的结果
    :param kwargs: 可指定源response，source=response
    :return:
    """
    if first:
        return _xpathF(response, xpath_rule)
    elif join:
        return _xpathJ(response, xpath_rule, **kwargs)
    elif returnList:
        return _xpathE(response, xpath_rule)
    elif url:
        return _xpath_hyperlinks(response, xpath_rule, url=True, **kwargs)
    elif urls:
        return _xpath_hyperlinks(response, xpath_rule, urls=True, **kwargs)
    elif article:
        return _get_article(response, xpath_rule, **kwargs)
    else:
        return _xpath(response, xpath_rule)


def _xpath(response, xpath_rule):
    return response.xpath(xpath_rule)


def _xpathF(response, xpath_rule):
    return response.xpath(xpath_rule).extract_first()


def _xpathE(response, xpath_rule):
    return response.xpath(xpath_rule).extract()


def _xpathJ(response, xpath_rule, sep="", stripEach=True, stripEnd=True):
    """
    使用extract获取list，并根据参数join合并
    :param response: --
    :param xpath_ruler: 数据获取的xpath规则
    :param sep: 合并时join使用的参数，默认为""
    :param stripEach: 是否对每一行执行strip
    :param stripEnd: 是否对结果执行strip
    :return:
    """
    list = response.xpath(xpath_rule).extract()
    if stripEach:
        list = [row.strip() for row in list]
        return sep.join(list)
    res = sep.join(list)
    return res.strip() if stripEnd else res


def _xpath_hyperlinks(response, xpath_rule, url=False, urls=False, **kwargs):
    if url:
        hyperlinks = _xpathF(response, xpath_rule)
        response = kwargs.get("source", response)
        return response.urljoin(hyperlinks) if hyperlinks else None
    elif urls:
        hyperlinks = _xpathE(response, xpath_rule)
        response = kwargs.get("source", response)
        return [response.urljoin(each) for each in hyperlinks if each]


def _get_article(response, xpath_rule, **kwargs):
    html_text = data_from_xpath(response, xpath_rule, join=True, **kwargs) \
        .replace("\r\n", " ").replace("\n", " ")
    html_text = _unescape(html_text)
    text = _transform_html_to_text(html_text, **kwargs)
    return arrayJoin(text, func=lambda x: x.strip(), strict=True, sep='\n', sepJ='\n')


def _transform_html_to_text(html_text, div_is_line=True, **kwargs):
    html_text = re.sub('<p.*?>|</p>|<br.*?>|</br>|<tr.*?>|</tr>', '\n', html_text, flags=re.S)
    html_text = re.sub('<td.*?>|</td>|<th.*?>|</th>', ' ', html_text, flags=re.S)
    if div_is_line:
        html_text = re.sub('<div.*?>|</div>', '\n', html_text, flags=re.S)
    res = re.sub('<.*?>', '', html_text, flags=re.S)
    return res


def _unescape(html_text):
    return html.unescape(html_text)
