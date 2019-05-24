import requests
import json

from scrapy import Selector

from english2china import list2china, get_data
from SHIPS_NAME import names

url = "http://track.logink.org:9082/OceanTracking/VesselTracking"

server_provider_url = "htt" \
                      "p://track.logink.org/vesselJSON.jsp"
# res = requests.get(server_provider_url)
# response = Selector(text=res.text)
# server_provider = response.xpath('//div[@id="detail_table"]//tr[position()>1]/td[2]/text()').extract()


# server_provider = ['CNNGB', 'CNZOS', 'CNWNZ', 'CNDAL', 'COSCO', 'CARGOSMART', 'NBEPORT', 'ZJEPORT', 'CNZUH', 'AEKHL', 'BBGP',
#         'COLINS', 'SPIDC']
# 异常：'CNWNZ', 'CNDAL', 'COSCO', 'NBEPORT', 'ZJEPORT', 'AEKHL', 'COLINS', 'SPIDC'
server_provider = ['COSCO']

for server in server_provider:
    temp = []
    # for test in
    for line in names.strip().split("\n"):
        try:
            line = line.strip()
            res1 = requests.get(url, params=get_data(line, server), timeout=0.5)
            info = json.loads(res1.text)
            if info["status"] == "Null":
                print(line, info["error"])
            elif info["status"] == "False":
                print(line, info["error"])
            elif info["status"] == "Exception":
                print(line, info["error"])
            else:
                temp.append(info)
                with open('%s-test1.json' % server, "a", encoding="utf8") as test_f:
                    test_f.write(json.dumps(info, ensure_ascii=False))
        except requests.exceptions.ReadTimeout:
            print('%s ### time out...' % line)
    with open("%s-船舶状态查询.json" % server, "w", encoding="utf8") as f:
        f.write(json.dumps(temp, ensure_ascii=False))
    with open("%s-船舶状态查询-中文.json" % server, "w", encoding="utf8") as f:
        f.write(json.dumps(list2china(temp), ensure_ascii=False))
