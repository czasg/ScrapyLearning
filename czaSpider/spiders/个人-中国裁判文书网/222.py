import execjs

import requests


# url = "http://wenshu.court.gov.cn/Index"
# res = requests.get(url, headers=headers)
# print(res.headers)
# # print(res.text)
#
# print('###' * 50)
#
# key = "V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDYyNTE0MjE="
# # url = "http://wenshu.court.gov.cn/Index?wzwschallenge={}"  # V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDgyNzI2OTU=
# url = "http://wenshu.court.gov.cn/WZWSREL0luZGV4?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDcxMTQwMjE="
# res = requests.get(url, headers=headers)
# print(res.headers)
# # print(res.text)
#
# print('###' * 50)
# headers = {
#     "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
# "Accept-Encoding":"gzip, deflate",
# "Accept-Language":"zh-CN,zh;q=0.9",
# "Connection":"keep-alive",
# "Cookie":"wzws_cid=0e84b9edc4e98899d850a4e4234f8e58e9103042d0df86a20891e21860dd93c7c037243cf73eb78ccf333fcf958f7693bd3265f40d0246b6673f0b345bfe6a6c",
# "Host":"wenshu.court.gov.cn",
# "Referer":"http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6",
# "Upgrade-Insecure-Requests":"1",
# "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
# }
#
# param = {
# "sorttype":"1",
# "conditions":"searchWord 1  刑事案件 案件类型:刑事案件",
# }
# url = "http://wenshu.court.gov.cn/Index"
# res = requests.get(url, params=param, headers=headers)
# print(res.headers)


# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
# }
# # url = "http://wenshu.court.gov.cn/Index"
# url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
# res = requests.get(url, headers=headers)
# print(res.headers)
# print(res.text)



# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
#     "Cookie":"wzws_cid=d30a93477e10eb812c6622e0b870aecc525c4a96de4274eebea128bd39a2bb0ed09e6bd4c737332697df128831d7770b0f2957907cd403b88fb9b2fe106c17709cce28bf3189c97faed94083566078babe3acaa6777c0dcb7b8f972457fc5771"
# }
# # url = "http://wenshu.court.gov.cn/WZWSREL0luZGV4?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDIwMDkyMTE="
# url = "http://wenshu.court.gov.cn/WZWSREL0xpc3QvTGlzdD9zb3J0dHlwZT0xJmNvbmRpdGlvbnM9c2VhcmNoV29yZCsxKyslRTUlODglOTElRTQlQkElOEIlRTYlQTElODglRTQlQkIlQjYrJUU2JUExJTg4JUU0JUJCJUI2JUU3JUIxJUJCJUU1JTlFJThCOiVFNSU4OCU5MSVFNCVCQSU4QiVFNiVBMSU4OCVFNCVCQiVCNg==?wzwschallenge=V1pXU19DT05GSVJNX1BSRUZJWF9MQUJFTDEwODQ2Nzc2"
# res = requests.get(url, headers=headers)
# print(res.headers)
# print(res.text)
# print(res.url)
# print(res.request)
# print(res.cookies)

# ccd1728de5e7b5aeb345f29510505ed202c2a92657622e5c8fc36cbdfb1dd4b68033b5fea1da4bafae20c6dfa7836a595b8e901e42a39deadee8d377708842c1ed4fecc21d096b3e1ed52b9f39225dffc37273e4571a78bab92b2c4716535657

