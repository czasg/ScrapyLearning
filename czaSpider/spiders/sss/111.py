# from czaSpider.czaBaseSpider import IOCO
import execjs


with open('zgcpwsw1.js', encoding='utf-8') as f:
    js = f.read()
    eee = execjs.compile(js)
    res = eee.call('anti_first', "XxSZf<$.HVO`}^8z", "7923")
    print(res)

with open('zgcpwsw2.js', encoding='utf-8') as f:
    js = f.read()
    eee = execjs.compile(js)
    argv1,argv2,argv3 = eee.call('anti_second', "979932bd95ff92df4601ba1857622c0f2add658a")
    print(argv1,argv2,argv3)