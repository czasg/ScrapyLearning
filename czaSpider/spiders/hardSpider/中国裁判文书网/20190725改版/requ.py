import requests
import re
import execjs
from pprint import pprint


try:
    with open('zgcpwsw2.js', encoding='utf-8') as f:
        js = f.read()
        anti_second = execjs.compile(js)

    with open('zgcpwsw3.js', encoding='utf-8') as f:
        js = f.read()
        anti_third = execjs.compile(js)
except:
    pass

# url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
url = "http://oldwenshu.court.gov.cn/list/list/?sorttype=1&number=&guid=4918fb8a-0023-590f857d-fa7abd5a6f35&conditions=searchWord+QWJS+++%E5%85%A8%E6%96%87%E6%A3%80%E7%B4%A2:%E5%90%88%E5%90%8C%E8%AF%88%E9%AA%97"
# url = "http://oldwenshu.court.gov.cn/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
def refresh_formData(page, vl5x, number, guid):
    formData = {
        "Param": "案件类型:刑事案件",
        "Index": str(page),
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": str(vl5x),
        "number": 'oldw',
        "guid": str(guid),
    }
    return formData


if __name__ == '__main__':

    with requests.Session() as requests:
        response = requests.get(url, headers=headers)
        print(response.cookies.items())
        vjkl5 = re.search("vjkl5=(.*?);", str(response.headers)).group(1)
        print(f"vjkl5={vjkl5}")
        vl5x, guid, number = anti_second.call('anti_second', vjkl5)
        print(vl5x, guid, number)
        formData = refresh_formData(1, vl5x, number, guid)
        pprint(formData)
        pprint(headers)
        headers.update({
            "Connection": "keep-alive",
            "Content-Length": "237",
            "Host": "oldwenshu.court.gov.cn",
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        })
        # response1 = requests.post("http://wenshu.court.gov.cn/List/ListContent", data=formData, headers=headers)
        response1 = requests.post("http://oldwenshu.court.gov.cn/List/ListContent", data=formData, headers=headers)
        print(response1.status_code)
        print(response1.cookies.items())
        print(response1.content)


    # vl5x, guid, number = anti_second.call('anti_second', "e3afa1691ffe4e8a7014318a4861175201b83d7b")
    # print(vl5x, guid, number)
    # 6b5767bbaa309a44c1e91597
    # 6b5767bbaa309a44c1e91597


