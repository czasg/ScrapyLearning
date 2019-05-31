import execjs

from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

anti_js = None
try:
    with open("银监会0_1.js", encoding='utf-8') as f:
        js = f.read()
        anti_js = execjs.compile(js)
except:
    pass


class MySpider(IOCO):
    name = "银监会-银监分局"

    handle_httpstatus_list = [521]
    url = "http://www.cbrc.gov.cn/zhuanti/xzcf/get2and3LevelXZCFDocListDividePage//2.html?current=1"

    def parse(self, response):
        if re.match("<script>", response.text):
            print(response.text)
            cookie = anti_js.call("get_cookie", response.text.strip())
            print(cookie)
            test = re.search('__jsl_clearance=(.*)', anti_js.call("get_cookie", response.text.strip())).group(1)
            print(test)
            yield response.request.replace(dont_filter=True, cookies={"__jsl_clearance":test})
        else:
            print(response.text)

if __name__ == '__main__':
    MySpider.cza_run_spider()