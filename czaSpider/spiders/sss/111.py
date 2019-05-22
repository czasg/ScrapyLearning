# from czaSpider.czaBaseSpider import IOCO
import execjs


with open('zgcpwsw.js', encoding='utf-8') as f:
    js = f.read()
    eee = execjs.compile(js)
    res = eee.call('anti_first', "XxSZf<$.HVO`}^8z", "7923")
    print(res)

