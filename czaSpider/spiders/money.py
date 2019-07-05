import requests
import json
import re
import time

url = "https://dncapi.bqiapp.com/api/coin/web-coinrank?page=1&type=-1&pagesize=100&webp=1"  # 入口
temp = []  # 临时存放，用于过滤重复数据
results = []  # 最终数据


def next_page(url, format):  # 下一页url入口
    current_page_num = re.search(format.replace("%d", "(\d+)"), url).group(1)
    print('当前第%s页' % current_page_num)
    return re.sub(format.replace("%d", "(\d+)"), format % (int(current_page_num) + 1), url)


def main(url, file_name):
    res = requests.get(url)
    json_data = json.loads(res.text)
    new = 0
    for data in json_data['data']:
        fullname, current_price = data['fullname'], data['current_price']
        if fullname in temp:
            continue
        temp.append(fullname)
        new += 1
        results.append({fullname: current_price})
    if new:  # 是否有新数据，有则跳转下一页
        main(next_page(url, 'page=%d'), file_name)
    else:  # 保存结果
        with open(file_name, 'w', encoding='utf-8') as f_a:
            f_a.write(json.dumps(results, ensure_ascii=False))


if __name__ == '__main__':
    file_name = "币价%s.json" % int(time.time())
    main(url, file_name)
