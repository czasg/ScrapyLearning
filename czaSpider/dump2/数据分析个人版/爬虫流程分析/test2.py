import json
from collections import defaultdict

dupefilter = ['疑难网站', '网站异常', '驳回需求', '运维发现异常', '废弃需求', '停止维护', '网站异常']
basic_state = ['正在开发', '开发完成', '清洗修改完成', '正在测试', '测试查完成', '正在入库', '入库完成', '研发修改完成', '返回修改']
def get_data(name):
    with open('%s.json' % name, 'r', encoding='utf-8') as json_file:
        return json.loads(json_file.read())

def get_dupefilter_spider(data_list):
    dupefilter_spider = set()
    for data in data_list:
        if data['rwzt'] in dupefilter or data['spiderName'].count('-') != 2:
            dupefilter_spider.add(data['spiderName'])
    return dupefilter_spider
def get_task_state_statistics(data_list):
    statistics = dict()
    for data in data_list:
        statistics[data['rwzt']] = statistics.get(data['rwzt'], 0) + 1
    return statistics
def get_spider_tasks(data_list, dupefilter=()):
    spider_tasks = defaultdict(list)
    for data in data_list:
        if data['spiderName'] in dupefilter:
            continue
        spider_tasks[data['spiderName']].append(data)
    return spider_tasks
if __name__ == '__main__':
    # aim = "人事变动"
    # data = get_data(aim)
    # print(get_task_state_statistics(data[aim]))
    # filter_spider_name = get_dupefilter_spider(data[aim])
    # all_spider_tasks = get_spider_tasks(data[aim], filter_spider_name)
    # print(all_spider_tasks)

    def _test(data):
        print(data, type(data))

    _test([1,2,3])
    _test((1,2,3))
