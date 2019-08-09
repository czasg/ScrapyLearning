from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *

from six.moves.urllib.parse import urljoin
class MySpider(IOCO):
    name = "world-test111"
    parse_item = True
    clean_item = True
    # custom_settings = {'HTTPERROR_ALLOWED_CODES':[521, 502],
    #                    'DOWNLOADER_MIDDLEWARES':{'czaSpider.middlewares.anti_clearance.AntiJsClearanceMiddleware': 100}}
    # url = "http://huangpu.customs.gov.cn/huangpu_customs/536775/536795/xzcf77/hgzscqxzcfajxxgk98/index.html"
    # url = 'http://ghgtw.beijing.gov.cn/searches/searchForXingZhengChuFa?' \
    #       'nothing=nothing&nothing=nothing&pageBean.currentPage=1&pageBean.itemsPerPage=10'
    url = "http://ghzrzyw.beijing.gov.cn/col/col2791/index.html"

    # def start_requests(self):
    #     cookie = {
    #         "Cookie": "TSb95bd363_75=TSb95bd363_rc=1&TSb95bd363_id=5&TSb95bd363_cr=08f613d8afab28002a2151e24771cecbd9054c7773a64a432bbde3957c8a1127d75dedbe491341a6cd23691bacb49c89:08053e5be504a800b3201f513220c029a009d077660fa6e4541ea23c982404541fc8fa8920b34393dd8bc09d7323a6035d1e1646891f6c4fbed59afc10ba3678ad6e2c402db12722fbfaff0c6513793c1875fdcf9970ab12e8167101deafdf60b0d0f923ffe285eb144782771ce6bbf26b59692b656c61dae4b5f9650f7b916f7a318797b9642dd9d13e46cfdbced514e48f6621841649071a58b5297b3db1d36d4082315328b1cac63bd67f06df7a2d&TSb95bd363_ef=&TSb95bd363_pg=0&TSb95bd363_ct=0&TSb95bd363_rf=http%3a%2f%2fhuangpu.customs.gov.cn%2fhuangpu_customs%2f536775%2f536795%2fxzcf77%2fhgzscqxzcfajxxgk98%2findex.html;",
    #     }
    #     yield Request(self.url, headers=cookie)

    def parse(self, response):
        print(response.text)
        print(response.url)
        # with open('haha.html', 'w') as file:
        #     file.write(response.text)


if __name__ == '__main__':
    MySpider.cza_run_spider()
    # url = "http://huangpu.customs.gov.cn/huangpu_customs/536775/536795/xzcf77/hgzscqxzcfajxxgk98/index.html"
    # print(urljoin(url, '/TSPD/08f613d8afab2000dff7a6d1677e9311bae106874bff0d043359ba2e6e66a16e9123d1293de2448e?type=9'))