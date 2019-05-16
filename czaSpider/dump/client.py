import requests


url = "http://127.0.0.1:9000"


files = {"pyFile": open('text.txt', 'rb')}
res = requests.post(url, files=files)

print(res)
print(res.content)
print(res.text)
