# from selenium import webdriver
#
#
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gup')
# driver = webdriver.chrome(chrome_options=chrome_options)


# from czaSpider.czaBaseSpider import IOCO
# from czaSpider.czaTools import *
#
# class MySpider(IOCO):
#     name = 'test-caipanwenshu'
#
#     def start_requests(self):
#         url = "http://wenshu.court.gov.cn/list/list/"
#         data = {
#             "sorttype": "1",
#             "conditions": "searchWord 合同   关键词:合同",
#         }
#         yield FormRequest(url, method='GET', formdata=data)
#
#     def parse(self, response):
#         print(response.headers)
#
#
# if __name__ == '__main__':
#     MySpider.cza_run_spider()