import re
import execjs

from scrapy import Selector


def get_redirect_url(response):
    flag = "t" * 5
    se = Selector(text=response.text)
    js = se.xpath("//script/text()").get()
    js = re.sub("window\[.+?\('.+?','.+?'\)]", flag, js)
    js += "function cmd(){return " + flag + "}"
    ret = execjs.compile(js).call("cmd")
    return ret