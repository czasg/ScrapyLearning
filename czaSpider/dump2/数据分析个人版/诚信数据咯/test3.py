import json, numpy as np
from collections import defaultdict
tasks = ("诚信数据",)
demand_states = {'任务已分发', '驳回运维意见', '待处理'}
developer_states = {'初爬通过', '正在开发', '自查完成', '正在下载源码', '正在修改', '代码完成',
                    '解析完成', '请求撤回提交', '开发完成', '源码下载完成', '疑难网站',
                    '提交任务', '初爬完成', '研发修改完成', '驳回测试修改意见', '正在解析'}
cleaning_states = {'文件清洗完成', '正在清洗', '清洗修改完成'}
test_states = {'测试查完成', '测试挂起', '正在测试', '初测通过', '返回清洗修改', '返回修改', '请清洗文件', '请重新下源码', '源码有问题'}
storage_states = {'返回修改', '入库复核通过', '入库失败', '入库完成', '正在入库', '不入库', '数据已转移', '暂不入库', '重跑一遍', '重跑完成'}
operations_states = {'网站异常', '停止维护', '全网查完成', '无增量挂起', '废弃需求', '运维发现异常', '驳回需求'}
abandoned_states = {'停止维护', '废弃需求'}
complete_states = {'入库完成', '数据已转移', '入库复核通过'}
def get_data(*names):
    for name in names:
        with open('%s.json' % name, 'r', encoding='utf-8') as json_file:
            yield json.loads(json_file.read())[name]
def merge_data(*args):
    res = []
    sta = []
    for data in args:
        res.extend(data)
        sta.append(len(data))
    return res, sta
fina, stat = merge_data(*[data for data in get_data(*tasks)])
stat = dict(zip(tasks, stat))  # todo {'诚信数据': 25024}  这表示记录
def get_spider_tasks(data_list, dupefilter=()):
    spider_tasks = defaultdict(list)
    for data in data_list:
        if data['spiderName'] in dupefilter:
            continue
        spider_tasks[data['spiderName']].append(data)
    return spider_tasks
spider_tasks = get_spider_tasks(fina)
spider_tasks_statistics = {'诚信数据': len(spider_tasks)}  # todo {'诚信数据': 836}  这表示任务量
event_state = ['需求', '开发', '测试', '清洗', '测试', '入库', '运维']
event = []
event_name_value = dict()
operation_tasks = dict()
abandoned_tasks = dict()
storage_tasks = dict()
for spiderName, spider_task in spider_tasks.items():
    _event = [0 for _ in range(6)]
    if spider_task[-1]['rwzt'] in abandoned_states:
        abandoned_tasks.setdefault(spiderName, spider_task)
    for task in spider_task:
        if spiderName not in operation_tasks and task['rwzt'] in operations_states:
            operation_tasks.setdefault(spiderName, spider_task)
        if spiderName not in storage_tasks and task['rwzt'] in complete_states:
            storage_tasks.setdefault(spiderName, spider_task)
        for index, state in enumerate(
                [demand_states, developer_states, cleaning_states, test_states, storage_states, operations_states]):
            if task['rwzt'] in state:
                _event[index] = _event[index] + 1
                break
    event.append(_event)
    event_name_value.setdefault(spiderName, _event)
events = np.array(event)  # todo [[], [], []]  各个任务的统计次数
operation_tasks_statistics = {'诚信数据': len(operation_tasks)}  # todo {'诚信数据': 644}  经历过运维的任务
abandoned_tasks_statistics = {'诚信数据': len(abandoned_tasks)}  # todo {'诚信数据': 326}  处于废弃状态的任务
storage_tasks_statistics = {'诚信数据': len(storage_tasks)}  # todo {'诚信数据': 716}  历史入库完成的爬虫
abandoned_tasks_2 = dict()
abandoned_tasks_3 = dict()
abandoned_tasks_4 = dict()
for spiderName, spider_task in storage_tasks.items():
    for task in spider_task:
        if spiderName not in abandoned_tasks_2 and task['rwzt'] in operations_states:
            abandoned_tasks_2.setdefault(spiderName, spider_task)
        if spiderName not in abandoned_tasks_3 and task['rwzt'] in abandoned_states:
            abandoned_tasks_3.setdefault(spiderName, spider_task)
storage_tasks_2_statistics = {'诚信数据': len(abandoned_tasks_2)}  # todo {'诚信数据': 546}  历史入库完成的爬虫中, 76%左右的任务会经历运维
storage_tasks_3_statistics = {'诚信数据': len(abandoned_tasks_3)}  # todo {'诚信数据': 252}  历史入库完成的爬虫中，35%左右的任务会被废弃
for spiderName, spider_task in abandoned_tasks_3.items():
    if len(spider_task) > 1:
        time_diff = spider_task[-1]['time'] - spider_task[0]['time']
        abandoned_tasks_4.setdefault(spiderName, [time_diff//2592000, sorted(spider_task, key=lambda task: task['time'])[-1]['time']])
abandoned_tasks_4 = abandoned_tasks_4  # todo 被废弃任务所经历的时间，单位为月，可画散点图，此处还可插入运维次数就刚刚好了
abandoned_tasks_4_keys = set(abandoned_tasks_4.keys())
abandoned_tasks_4_value = {}
for spiderName, spider_task in event_name_value.items():
    if spiderName in abandoned_tasks_4_keys:
        abandoned_tasks_4_value[spiderName] = spider_task
abandoned_tasks_4 = sorted(abandoned_tasks_4.values(), key=lambda x: x[1])
print(abandoned_tasks_4)
import matplotlib
print(matplotlib.matplotlib_fname())
print(np.array([[0,0, 0],[0,0,0]]).shape)

