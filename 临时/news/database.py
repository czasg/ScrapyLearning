import jieba
import re
import json

from pymongo import MongoClient
from datetime import datetime, timedelta
from collections import defaultdict

area = {
    '北京': ['北京', '大兴区', '房山区', '怀柔区', '顺义区', '石景山区', '密云区', '平谷区', '延庆区', '门头沟区', '昌平区'],
    '上海': ['上海', '杨浦区', '松江区', '嘉定区'],
    '天津': ['天津', '静海区', '河北区', '津南区', '宝坻区', '南开区', '北辰区', '东丽区', '武清区'],
    '重庆': ['重庆', '渝北区', '秀山土家族苗族自治县', '武隆区', '永川区', '沙坪坝区'],
    '澳门': ['澳门'],
    '香港': ['香港'],
    '海南': ['海南', '海口', '三亚', '白沙黎族', '陵水黎族自治县', '文昌市', '澄迈县', '万宁市', '琼中黎族苗族自治县',
           '定安县', '河西区', '东方市'],
    '台湾': ['台湾', '台北', '高雄', '基隆', '台中', '台南', '新竹', '嘉义'],
    '河北': ['河北', '唐山', '邯郸', '邢台', '保定', '承德', '沧州', '廊坊', '衡水', '石家庄', '秦皇岛', '张家口'],
    '山西': ['山西', '太原', '大同', '阳泉', '长治', '晋城', '朔州', '晋中', '运城', '忻州', '临汾', '吕梁'],
    '山东': ['山东', '济南', '青岛', '淄博', '枣庄', '东营', '烟台', '潍坊', '济宁', '泰安', '威海', '日照', '莱芜', '临沂', '德州', '聊城', '滨州', '荷泽',
           '菏泽'],
    '江苏': ['江苏', '南京', '无锡', '徐州', '常州', '苏州', '南通', '淮安', '盐城', '扬州', '镇江', '泰州', '宿迁', '连云港'],
    '浙江': ['浙江', '杭州', '宁波', '温州', '嘉兴', '湖州', '绍兴', '金华', '衢州', '舟山', '台州', '丽水', '江北'],
    '安徽': ['安徽', '合肥', '芜湖', '蚌埠', '淮南', '淮北', '铜陵', '安庆', '黄山', '滁州', '阜阳', '宿州', '巢湖', '六安', '亳州', '池州', '宣城', '马鞍山'],
    '福建': ['福建', '福州', '厦门', '莆田', '三明', '泉州', '漳州', '南平', '龙岩', '宁德'],
    '江西': ['江西', '南昌', '萍乡', '新余', '九江', '鹰潭', '赣州', '吉安', '宜春', '抚州', '上饶', '景德镇'],
    '河南': ['郑州', '开封', '洛阳', '焦作', '鹤壁', '新乡', '安阳', '濮阳', '许昌', '漯河', '南阳', '商丘', '信阳', '周口', '驻马店', '济源', '平顶山',
           '三门峡'],
    '湖北': ['湖北', '武汉', '黄石', '襄樊', '十堰', '荆州', '宜昌', '荆门', '鄂州', '孝感', '黄冈', '咸宁', '随州', '恩施', '仙桃', '天门', '潜江',
           '江夏区', '江岸区', '黄陂区', '襄阳市', '新洲区', '武昌区', '青山区', '蔡甸区', '硚口区', '洪山区', '江汉区'],
    '湖南': ['湖南', '长沙', '株洲', '湘潭', '衡阳', '邵阳', '岳阳', '常德', '益阳', '郴州', '永州', '怀化', '娄底', '吉首', '张家界',
           '湘西土家族苗族自治州'],
    '广东': ['广东', '广州', '深圳', '珠海', '汕头', '韶关', '佛山', '江门', '湛江', '茂名', '肇庆', '惠州', '梅州', '汕尾', '河源', '阳江', '清远', '东莞',
           '中山',
           '潮州', '揭阳', '云浮'],
    '广西': ['广西', '南宁', '柳州', '桂林', '梧州', '北海', '钦州', '贵港', '玉林', '百色', '贺州', '河池', '来宾', '崇左', '防城港', '广西壮族自治区'],
    '四川': ['四川', '成都', '自贡', '泸州', '德阳', '绵阳', '广元', '遂宁', '内江', '乐山', '南充', '宜宾', '广安', '达州', '眉山', '雅安', '巴中', '资阳',
           '西昌',
           '攀枝花', '甘孜藏族自治州', '凉山彝族自治州'],
    '贵州': ['贵州', '贵阳', '遵义', '安顺', '铜仁', '毕节', '兴义', '凯里', '都匀', '六盘水', '黔西南布依族苗族自治州', '黔东南苗族侗族自治州', '黔南布依族苗族自治州'],
    '云南': ['云南', '昆明', '曲靖', '玉溪', '保山', '昭通', '丽江', '思茅', '临沧', '景洪', '楚雄', '大理', '潞西', '文山壮族苗族自治州',
           '红河哈尼族彝族自治州'],
    '陕西': ['陕西', '西安', '铜川', '宝鸡', '咸阳', '渭南', '延安', '汉中', '榆林', '安康', '商洛'],
    '甘肃': ['甘肃', '兰州', '金昌', '白银', '天水', '武威', '张掖', '平凉', '酒泉', '庆阳', '定西', '陇南', '临夏', '合作', '嘉峪关'],
    '辽宁': ['辽宁', '沈阳', '大连', '鞍山', '抚顺', '本溪', '丹东', '锦州', '营口', '盘锦', '阜新', '辽阳', '铁岭', '朝阳', '葫芦岛'],
    '吉林': ['吉林', '长春', '吉林', '四平', '辽源', '通化', '白山', '松原', '白城', '延吉', '延边朝鲜族自治州'],
    '黑龙江': ['黑龙江', '鹤岗', '鸡西', '大庆', '伊春', '黑河', '绥化', '双鸭山', '牡丹江', '佳木斯', '七台河''哈尔滨', '齐齐哈尔',
            '大兴安岭地区'],
    '青海': ['青海', '西宁', '德令哈', '格尔木', '黄南藏族自治州'],
    '宁夏': ['宁夏', '银川', '吴忠', '固原', '中卫', '石嘴山'],
    '西藏': ['西藏', '拉萨', '日喀则', '山南市', '林芝市'],
    '新疆': ['新疆', '哈密', '和田', '喀什', '昌吉', '博乐', '伊宁', '塔城', '吐鲁番', '阿图什', '库尔勒', '五家渠', '阿克苏', '阿勒泰', '石河子',
           '阿拉尔', '乌鲁木齐', '克拉玛依', '图木舒克', '巴音郭楞蒙古自治州', '北屯市', '伊犁哈萨克自治州', '克孜勒苏柯尔克孜自治州'],
    '内蒙古': ['内蒙古', '包头', '乌海', '赤峰', '通辽', '鄂尔多斯', '呼伦贝尔', '巴彦淖尔', '乌兰察布', '兴安盟', '呼和浩特', '锡林郭勒盟',
            '阿拉善盟', '巴彦淖尔盟', '乌兰察布盟'],
}


def choose_province(city):
    for name, values in area.items():
        for value in values:
            if city.startswith(value):
                return name
    raise Exception('没有找到对应的省份：' + city)


class Mongodb:
    def __init__(self, online=False):
        self._client = None
        self.online = online
        self.connect_mongodb()

    @property
    def client(self):
        assert self._client, 'Mongodb Client Cannot Be None!'
        return self._client

    def connect_mongodb(self):
        if self.online:
            online_paras = {
                "host": ["192.168.0.31", "192.168.0.32", "192.168.0.33", ],
                "port": 23333,
                "replicaSet": "data_online",
                "readPreference": "secondaryPreferred",

                "username": "taohui",
                "password": "zhengwubaike",
            }
        else:
            online_paras = {
                "host": "192.168.0.91",
                "port": 27017,
                "readPreference": "secondaryPreferred",
            }
        self._client = MongoClient(**online_paras)


mongodb = Mongodb(online=True)
mongodb_offline = Mongodb(online=False)
now = datetime.now()
today = datetime(now.year, now.month, now.day)
yesterday = today - timedelta(days=1)
RE_SEARCH = re.compile('.*?-(.*?)-').search


def get_collection_count_yesterday(db='新闻(新闻)', filter_db='', filter_keys=None):
    result = defaultdict(dict)
    db_handler = mongodb.client[db]
    collections = db_handler.list_collection_names()
    for collection in collections:
        try:
            if collection.startswith(filter_db):
                result[collection]['titles'] = []
                jieba_list = []
                for doc in db_handler[collection].find(
                        {'$and': [{'发布日期': {'$gt': yesterday}}, {'发布日期': {'$lt': today}}]},
                        dict(zip(filter_keys, [1 for _ in range(len(filter_keys))]), _id=0) if filter_keys else None):
                    result[collection]['titles'].append(doc)
                    jieba_list.extend(jieba.lcut(doc[filter_keys[0]])) if filter_keys else None
                result[collection]['count'] = result[collection]['titles'].__len__()
                result[collection]['name'] = RE_SEARCH(collection).group(1)
                result[collection]['timestamp'] = int(today.timestamp())
                result[collection]['province'] = choose_province(result[collection]['name'])
                mongodb_offline.client[db + '-offline-cza'][collection].update_one(
                    {'timestamp': result[collection]['timestamp']},
                    {'$set': dict(**result[collection], jieba_list=json.dumps(jieba_list, ensure_ascii=False))},
                    upsert=True)
        except Exception as e:
            print(e)
            continue
    mongodb.client.close()
    mongodb_offline.client.close()
    return result


if __name__ == '__main__':
    get_collection_count_yesterday(db='新闻(新闻)', filter_db='人民政府', filter_keys=['标题'])
