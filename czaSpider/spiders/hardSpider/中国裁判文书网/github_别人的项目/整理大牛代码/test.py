from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

from util import *


class MySpider(IOCO):
    name = "chinaReferee3-government"
    key = "全文检索:合同"

    ajax_url = "http://wenshu.court.gov.cn/website/parse/rest.q4w"

    def start_requests(self):
        query = "合同"
        yield FormRequest(self.ajax_url, formdata=get_list_form_data(query, pageSize=10))

    def parse(self, response):
        print(response.text)
        # list_content = get_detail_json(response)
        # doc_ids = list_content['relWenshu']
        # for doc_id in doc_ids:
        #     print(doc_id)


if __name__ == '__main__':
    MySpider.cza_run_spider()
