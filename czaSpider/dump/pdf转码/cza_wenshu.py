import requests
import re
import json


if __name__ == '__main__':
    # test = {'cza': 'test'}
    # test1 = '{"cza": "te"st"}'
    # print(json.dumps(test))
    # print(json.loads(test1))

    html = requests.get('http://192.168.0.243:9333/407,7345445500ee0fba9dc65e7e').text
    data = re.search('var jsonHtmlData = \"(.*)\";', html).group(1)
    data = data.replace("\\", "").replace('type="text/javascript"', '')
    print(data)
    print(data[2973:])

    print(json.loads(data))
