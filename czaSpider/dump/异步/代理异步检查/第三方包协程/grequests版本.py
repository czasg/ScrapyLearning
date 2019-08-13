import grequests

request_list = [
    grequests.get('https://www.baidu.com'),
    grequests.get('http://www.sina.com.cn'),
    grequests.get('https://news.baidu.com'),
]
# ##### 执行并获取响应列表 #####
response_list = grequests.map(request_list,size=5)
print(response_list)

# pip install grequests