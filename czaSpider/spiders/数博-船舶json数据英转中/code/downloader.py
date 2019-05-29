import requests
import json

from scrapy import Selector

from importlib import import_module

list2china = getattr(import_module("english2china"), "list2china")
names = getattr(import_module("SHIPS_NAME"), "names")

url = "http://track.logink.org:9082/OceanTracking/VesselTracking"

# server_provider = ['CNNGB', 'CNZOS', 'CNWNZ', 'CNDAL', 'COSCO', 'CARGOSMART', 'NBEPORT', 'ZJEPORT', 'CNZUH', 'AEKHL', 'BBGP',
#         'COLINS', 'SPIDC']
server_provider = ['COSCO']  # 服务商代号


# todo, 服务商获取，仅适配了船舶状态的url，其他是否需相同
def get_service():
    server_provider_url = "http://track.logink.org/vesselJSON.jsp"
    res = requests.get(server_provider_url)
    response = Selector(text=res.text)
    server_provider = response.xpath('//div[@id="detail_table"]//tr[position()>1]/td[2]/text()').extract()
    return server_provider


# json请求FormData
def get_data(name, PartyFunctionCode):
    data = {
        "method": "logink.track.vessel",
        "result_format": "1",
        "charset": "utf-8",
        "biz_version": "",
        "sec": {"userid": "901001",
                "token": "NmRkOTdjODQtMjMyYy00NzM4LWI2NmMtOGUxNTcwZTNiNDAwVF9UXzBBU19JRF9sb2dpbmtfMA"},
        "biz_content": {
            "SearchTypeCode": "13",
            "vesselEnglishName": name,
            "VesselCallNumber": "",
            "IMONumber": "",
            "VoyageNumber": "",
            "PortCode": "",
            "StartTime": "2019-01-01 00:00:00",
            "EndTime": "2019-5-24 23:59:59",
            "PartyFunctionCode": PartyFunctionCode,
            "CarrierName": ""},
    }
    return {k: str(v) for k, v in data.items()}


def main(timeout=0.7):
    # 遍历服务商，获取数据，超时为0.7s
    for server in server_provider:
        temp = []
        for line in names.strip().split("\n"):
            try:
                line = line.strip()
                res1 = requests.get(url, params=get_data(line, server), timeout=timeout)
                info = json.loads(res1.text)
                if info["status"] == "Null":
                    print(line, info["error"])
                elif info["status"] == "False":
                    print(line, info["error"])
                elif info["status"] == "Exception":
                    print(line, info["error"])
                else:
                    temp.append(info)
            except requests.exceptions.ReadTimeout:
                print('%s ### time out...' % line)
        # 保存原版
        with open("%s-船舶状态查询.json" % server, "w", encoding="utf8") as f:
            f.write(json.dumps(temp, ensure_ascii=False))
        # 保存中文
        with open("%s-船舶状态查询-中文.json" % server, "w", encoding="utf8") as f:
            f.write(json.dumps(list2china(temp), ensure_ascii=False))


if __name__ == "__main__":
    main()
