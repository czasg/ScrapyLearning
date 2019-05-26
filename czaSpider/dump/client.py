import requests


# url1 = "http://127.0.0.1:9000/upload/file"
# files = {"": open('test.py', 'rb')}
# res = requests.post(url1, files=files)

# 00155818274471048d003c032294d7ba452445c38ebe9e4000
# 0015582625774337b8fd5529d0b416691787d8362f97738000
if __name__ == "__main__":
    url2 = "http://127.0.0.1:9000/fetch/00155818274471048d003c032294d7ba452445c38ebe9e4000"
    res = requests.get(url2)

    print(res.status_code)
    print(res.text)
