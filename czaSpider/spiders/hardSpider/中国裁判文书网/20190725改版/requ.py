import requests
import re
import execjs


try:
    with open('zgcpwsw2.js', encoding='utf-8') as f:
        js = f.read()
        anti_second = execjs.compile(js)

    with open('zgcpwsw3.js', encoding='utf-8') as f:
        js = f.read()
        anti_third = execjs.compile(js)
except:
    pass

url = "http://wenshu.court.gov.cn/List/List?sorttype=1&conditions=searchWord+1++%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6+%E6%A1%88%E4%BB%B6%E7%B1%BB%E5%9E%8B:%E5%88%91%E4%BA%8B%E6%A1%88%E4%BB%B6"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
}
def refresh_formData(page, vl5x, number, guid):
    formData = {
        "Param": "全文检索:合同",
        "Index": str(page),
        "Page": "10",
        "Order": "法院层级",
        "Direction": "asc",
        "vl5x": str(vl5x),
        "number": str(number),
        "guid": str(guid),
    }
    return formData


if __name__ == '__main__':

    response = requests.get(url, headers=headers)
    vjkl5 = re.search("vjkl5=(.*?);", str(response.headers)).group(1)
    vl5x, guid, number = anti_second.call('anti_second', vjkl5)
    print(vl5x, guid, number)
    headers['Cookie'] = response.headers['Set-Cookie']
    formData = refresh_formData(1, vl5x, number, guid)
    print(formData)
    response1 = requests.post("http://wenshu.court.gov.cn/List/ListContent", data=formData, headers=headers)
    print(response1.status_code)
    print(response1.text)


