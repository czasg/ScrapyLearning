from czaSpider.czaBaseSpider import IOCO
from czaSpider.czaTools import *


class MySpider(IOCO):
    name = "中国裁判文书网-中国裁判文书网"

    ajax_url = "http://wenshu.court.gov.cn/website/parse/rest.q4w"

    def start_requests(self):
        self.mode = self.crawler.settings.get("mode")
        self.keyword = self.crawler.settings.get("target")
        if self.keyword:
            if self.mode == "1":
                self.query = [{"key": "s2", "value": self.keyword}]
            elif self.mode == "2":
                self.query = [{"key": "s21", "value": self.keyword}]
            self.logger.info("获取到了新的查询条件：%s", self.keyword)
            yield FormRequest(self.ajax_url, formdata=get_list_postData(self.query))
        else:
            self.logger.info("没有获取到查询条件")

    def parse(self, response):
        list_content = get_detail_json(response)
        for docId in list_content['relWenshu']:
            yield FormRequest(self.ajax_url, formdata=get_detail_postData(docId), callback=self.parse_detail)
            return  # test

    def parse_detail(self, response):
        info = {}
        detail_content = get_detail_json(response)
        for key, value in detail_content.items():
            if key in dict_map:
                info[dict_map[key]] = value
        import pprint
        pprint.pprint(info)


if __name__ == '__main__':
    MySpider.cza_run_spider()
    # import requests
    # data = {
    #     "docId": "692902dbddd44d3aa8bdaac40123726a",
    #     "ciphertext": "1100001 1010011 1110010 1000110 110010 1101100 1000111 110011 1000111 110000 110011 1100010 1101001 1110110 1001001 1111000 1101111 1110110 1010100 1111000 1110101 1100100 110110 110100 110010 110000 110001 111001 110000 111001 110001 110110 1010101 1100110 1010101 110100 1100010 1100111 1110011 1101111 1111001 1110011 1101111 1011010 1010011 111001 1011010 1010010 1101100 1011001 1010100 1010010 1110010 1000001 111101 111101",
    #     "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
    #     "__RequestVerificationToken": "zJRFVTItlCdULPkOpIzp34qS",
    # }
    # header = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.6 Safari/537.36'
    # }
    # print(requests.post('http://wenshu.court.gov.cn/website/parse/rest.q4w?HifJzoc9=4APPHXaWEu_Wki5oEkp_8JdCz6B9AkKVL62_Pyk7_nyPnsCBVAHTSsWmub9983DXruf7Xue5W7DFd269oq7q_nwbG7.lcGN8eB6XWyIJsVq1OiaN0uQNsNIwFChn6yYJAlxHY1R4YU0oM450KDrZMDu.PLtxAJll0swjCAGoPVo6sL1MJLZYV4Dis9WTz.IPm6ROldrhfl.dve2B3sLq2WaZ0yUqWJ42TOyqLRMo7qWtuXnCLiE3UiWU1TrtxSbQoB7xnBf52GYcYsptRoO.1oXHG2deB35G_86F.Bs.sMb_cAkWARym9iaHGU1UqlBx3f23Ytwvfqwp__luqjOrkyT7wSFrpbzfz5AQ8MYyr1fPnoXvdAICvE8gU8Vma7Jryte9',
    #                     data=data,headers=header).text)
