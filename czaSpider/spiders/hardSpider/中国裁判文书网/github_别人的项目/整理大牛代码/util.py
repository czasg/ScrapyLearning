import base64
import json
import logging
import math
import random
from datetime import datetime

from Cryptodome.Cipher import DES3  # pip install pycryptodomex
from Cryptodome.Util.Padding import pad, unpad

logger = logging.getLogger(__name__)

dict_map = {
    "s1": "案件名称",
    "s2": "法院名称",
    "s3": "审理法院",
    "s4": "法院层级",
    "s5": "文书ID",
    "s6": "文书类型",
    "s7": "案号",
    "s8": "案件类型",
    "s9": "审判程序",
    "s10": "审判程序",
    "s11": "案由",
    "s12": "案由",
    "s13": "案由",
    "s14": "案由",
    "s15": "案由",
    "s16": "案由",
    "s17": "当事人",
    "s18": "审判人员",
    "s19": "律师",
    "s20": "律所",
    "s21": "全文",
    "s22": "首部",
    "s23": "诉讼记录",
    "s24": "诉控辩",
    "s25": "事实",
    "s26": "理由",
    "s27": "判决结果",
    "s28": "尾部",
    "s29": "法律依据",
    "s30": "",
    "s31": "裁判日期",
    "s32": "不公开理由",
    "s33": "法院省份",
    "s34": "法院地市",
    "s35": "法院区县",
    "s36": "审理法院",
    "s37": "审理法院",
    "s38": "审理法院",
    "s39": "审理法院",
    "s40": "审理法院",
    "s41": "发布日期",
    "s42": "裁判年份",
    "s43": "公开类型",
    "s44": "案例等级",
    "s45": "关键字",
    "s46": "结案方式",
    "s47": "法律依据",
    "s48": "上网时间",
    "s49": "案例等级排序",
    "s50": "法院层级排序",
    "s51": "裁判日期排序",
    "s52": "审判程序排序",
    "s53": "当事人段",
    "s54": "其他",
    "cprqStart": "裁判日期开始时间",
    "cprqEnd": "裁判日期结束时间",
    "swsjStart": "上网时间开始时间",
    "swsjEnd": "上网时间结束时间",
    "flyj": "法律依据",
    "cprq": "裁判日期"
}


def get_list_form_data(query, page=1, pageSize=5):
    return {
        'pageId': get_pageId(),
        's8': '03',  # 全文检索条件下，此参数不影响
        'sortFields': 's51:desc',  # 按时间排序
        'ciphertext': get_ciphertext(),
        'pageNum': str(page),
        'pageSize': str(pageSize),
        'queryCondition': json.dumps(query),
        'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
        '__RequestVerificationToken': get_RequestVerificationToken()
    }


URL1 = "http://wenshu.court.gov.cn/content/content?DocID="
URL2 = "http://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId="


def docid_filter(docId):
    return {"$or": [{"URL": URL2 + docId},
                    {"URL": URL1 + '-'.join([docId[:8], docId[8:12], docId[12:16], docId[16:20], docId[20:]])}]}


def get_detail_postData(docId):
    return {
        "docId": docId,
        "ciphertext": get_ciphertext(),
        "cfg": "com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@docInfoSearch",
        "__RequestVerificationToken": get_RequestVerificationToken(),
    }


def validate_json(text):
    json_data = json.loads(text)
    if json_data['code'] != 1:
        raise Exception('请求失败：%s' % json_data['description'])
    return json_data


def good_content(text):
    try:
        validate_json(text)
        return True
    except:
        logger.warning("下载失败: %s" % text)
        return False


# 解密json数据 #
def get_detail_json(response):
    json_data = validate_json(response.text)
    if json_data["result"]:
        return json.loads(des3decrypt(cipher_text=json_data["result"],
                                      key=json_data["secretKey"],
                                      iv=datetime.now().strftime("%Y%m%d")))


# 获取随机token #
def get_RequestVerificationToken(size=24):
    arr = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    return ''.join(arr[round(random.random() * (len(arr) - 1))] for _ in range(size))


# 获取随机pageId #
def get_pageId():
    return ''.join(hex(math.floor(random.random() * 16))[2:] for _ in range(32))


# 获取随机ciphertext #
def des3encrypt(plain_text: str, key: str, iv: str) -> str:
    des3 = DES3.new(key=key.encode(), mode=DES3.MODE_CBC, iv=iv.encode())
    encrypted_data = des3.encrypt(pad(plain_text.encode(), DES3.block_size))
    cipher_text = base64.b64encode(encrypted_data).decode()
    return cipher_text


def des3decrypt(cipher_text: str, key: str, iv: str) -> str:
    des3 = DES3.new(key=key.encode(), mode=DES3.MODE_CBC, iv=iv.encode())
    decrypted_data = des3.decrypt(base64.b64decode(cipher_text))
    plain_text = unpad(decrypted_data, DES3.block_size).decode()
    return plain_text


def str2binary(string):
    return ' '.join(bin(ord(item))[2:] for item in string)


def get_ciphertext():
    now = datetime.now()
    timestamp = str(int(now.timestamp() * 1000))
    salt = get_RequestVerificationToken()
    iv = now.strftime("%Y%m%d")
    enc = des3encrypt(plain_text=timestamp, key=salt, iv=iv)
    return str2binary(salt + iv + enc)
