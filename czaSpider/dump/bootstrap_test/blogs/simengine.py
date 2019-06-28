import re
import json
import jieba
import pymysql

reObj = re.compile('[\s()（）~!@#$%^&*_+\-=/,.;:：\'、{}\[\]"<>|?。，“”\\\]')


class SimEngine:
    _invertedIndex = {}
    _result = []

    def __init__(self, **kwargs):  # 数据库初始化配置 #
        self.host = kwargs.get('host', 'localhost')
        self.user = kwargs.get('user', 'root')
        self.password = kwargs.get('password', 'cza19950917')
        self.db = kwargs.get('db', 'cza')
        self.table = kwargs.get('table', 'blogs')
        self.keys = kwargs.get('keys', ['name', 'summary'])
        self.primary_key = kwargs.get('primary_key', 'id')

    @property
    def invertedIndex(self):
        return self._invertedIndex

    @property
    def result(self):
        return self._result

    def init(self, path='invertedIndex.json'):  # 执行初始化
        self.init_label()  # 初始化倒排索引
        self.save_invertedIndex(path)  # 保存索引到json

    def init_label(self):
        db = pymysql.connect(self.host, self.user, self.password, self.db)
        cursor = db.cursor(pymysql.cursors.DictCursor)
        cursor.execute("select * from %s" % self.table)
        docs = cursor.fetchall()
        for doc in docs:
            label = ''
            for key in self.keys:
                label += doc.get(key, '')
            self._process_label(label, doc[self.primary_key])

    def _process_label(self, label, primary_key):
        for key in set(jieba.lcut(reObj.sub('', label))):
            val = self._invertedIndex.get(key) or []
            val.append(primary_key)
            self._invertedIndex[key.lower()] = val

    def save_invertedIndex(self, path):
        with open(path, 'w', encoding='utf-8') as fw:
            fw.write(json.dumps(self._invertedIndex, ensure_ascii=False))

    @classmethod
    def search(cls, user_input, path='invertedIndex.json'):
        cls._result = []
        cls._init_invertedIndex(path)
        cls._get_result(user_input)
        return cls._result

    @classmethod
    def _init_invertedIndex(self, path):
        with open(path, 'r', encoding='utf-8') as fr:
            self._invertedIndex = json.loads(fr.read())

    @classmethod
    def _get_result(cls, user_input):
        for key in set(jieba.lcut(reObj.sub('', user_input))):
            if key in cls._invertedIndex:
                cls._result.extend(cls._invertedIndex[key])
        for key in cls._invertedIndex:
            if user_input in key:
                cls._result.extend(cls._invertedIndex[key])


if __name__ == '__main__':
    SimEngine().init()
    # print(SimEngine.search('scrapy'))