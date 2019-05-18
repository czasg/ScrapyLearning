import requests


url = "http://127.0.0.1:9000/upload/file"


files = {"": open('test.py', 'rb')}
res = requests.post(url, files=files)

print(res.status_code)
print(res.content)
print(res.text)
