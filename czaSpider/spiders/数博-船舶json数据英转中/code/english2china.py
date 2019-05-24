




MAP_KEY = {
    "biz_result": "返回业务报文内容",
    "method": "业务类型",
    "sec": "安全信息段组",
    "userid": "物流交换代码",
    "token": "用户令牌",
    "charset": "编码类型",
    "result_encrptype": "加密类型",
    "result_format": "返回报文格式类型",
    "biz_sign": "签名串",
    "biz_version": "业务报文版本号",
    "ResultCode": "结果代码",
    "InformationList": "信息列表",
    "PartyFunctionCode": "参与方功能代码",
    "PartyIdentifier": "参与方标识符",
    "PartyName": "参与方名称",
    "VesselInformation": "船舶信息",
    "ShippingCompanyCode": "船公司代码",
    "VesselCallNumber": "船舶呼号",
    "IMONumber": "IMO编号",
    "vesselEnglishName": "船舶英文名称",
    "VesselStatusInformation": "船舶状态信息",
    "ImExIdentifier": "进出口标识符",
    "VoyageNumber": "航次",
    "DirectionCode": "方向代码",
    "SeaRouteCode": "航线代码",
    "TransportStatusCode": "运输状态代码",
    "DateOrTimeOrPeriod": "日期/时间/期限",
    "TimeZoneIdentifier": "时区标识符",
    "PlaceLocationQualifier": "地点/位置限定符",
    "PlaceOrLocationIdentification": "地点/位置标识",
    "PlaceOrLocation": "地点/位置",
    "StartDateTimeOfEnteringContainerYard": "进箱开始日期时间",
    "EndDateTimeOfEnteringContainerYard": "进箱截止日期时间",
    "Remark": "备注",
}

MAP_STATUS = {
    "951": "预计到港",
    "952": "预计离港",
    "40": "实际到港",
    "1": "实际靠泊",
    "24": "实际离港"
}


def dict2china(json_dict: dict) -> dict:
    translation = {}
    for key, value in json_dict.items():
        if key in MAP_KEY:
            key = MAP_KEY[key]
            if isinstance(value, dict):
                value = dict2china(value)
            if isinstance(value, list):
                value = list2china(value)
            if key == "运输状态代码":
                value = MAP_STATUS[value]
            translation[key] = value
    return translation


def list2china(json_list: list) -> list:
    return [dict2china(json) for json in json_list]


def get_data(name, PartyFunctionCode):
    data = {
        "method": "logink.track.vessel",
        "result_format": "1",
        "charset": "utf-8",
        "biz_version": "",
        "sec": {"userid": "901001",
                "token": "NmRkOTdjODQtMjMyYy00NzM4LWI2NmMtOGUxNTcwZTNiNDAwVF9UXzBBU19JRF9sb2dpbmtfMA"},
        "biz_content": {
            "SearchTypeCode":"13",
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
