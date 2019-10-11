import json, numpy as np, re, time
from collections import defaultdict, OrderedDict
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
print(stat)
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
# print(abandoned_tasks_4)
# import matplotlib
# print(matplotlib.matplotlib_fname())
# print(np.array([[0,0, 0],[0,0,0]]).shape)

life_time = {}  # todo 这是一个总统计图，很不错
for spiderName, spider_task in abandoned_tasks_2.items():  # 遍历每一个爬虫
    start_time = None  #
    first = None  #
    last = None  #
    total_times = 0  # 这个应该是用时间算出来的
    abnormal_times = None  #
    life_time_statistics = dict()
    for task in spider_task:  # 遍历所有的任务。
        if first and task['rwzt'] in operations_states:
            life_time_statistics.setdefault('last_time', task['time'])
            life_time_statistics['abnormal_times'] = life_time_statistics.get('abnormal_times', 0) + 1
            continue
        if start_time and task['rwzt'] in operations_states:
            first = True
            life_time_statistics.setdefault('first_time', task['time'])
            life_time_statistics.setdefault('last_time', task['time'])
            life_time_statistics['abnormal_times'] = life_time_statistics.get('abnormal_times', 0) + 1
        if task['rwzt'] in complete_states:
            start_time = True
            life_time_statistics.setdefault('start_time', task['time'])  # 记录第一次的时间
    if not life_time_statistics.get('first_time'):
        continue
    if spiderName in abandoned_tasks_3:
        life_time_statistics['total_times'] = ((life_time_statistics['last_time'] - life_time_statistics['start_time']) // 2592000) or 1
    else:
        life_time_statistics['total_times'] = ((time.time() - life_time_statistics['start_time']) // 2592000) or 1
    if life_time_statistics['total_times'] >= life_time_statistics['abnormal_times']:
        life_time.setdefault(spiderName, life_time_statistics)
# print(life_time)

# from datetime import datetime
import datetime
abnormal_analysis = {}
for spiderName, spider_task in abandoned_tasks_2.items():  # 遍历每一个已入库爬虫
    if len(spider_task) > 1:
        start_time = None
        _abnormal_analysis = {}
        time_format = '%d年%d月'
        for task in spider_task:  # 遍历所有的任务。
            # if not start_time and task['rwzt'] in complete_states:
            #     start_time = task['time']  # 拿到了开始时间，到最后一次结束，自动补全
            #     if spiderName in abandoned_tasks_3:  # 这里表示此爬虫是属于废弃爬虫的
            #         ...
            #     continue
            # if start_time:
            current_time = datetime.datetime.fromtimestamp(task['time'])
            current_year = current_time.year
            current_month = current_time.month
            current = time_format % (current_year, current_month)
            if task['rwzt'] in operations_states:
                _abnormal_analysis[current] = 1
        if _abnormal_analysis:
            abnormal_analysis.setdefault(spiderName, _abnormal_analysis)
# print(abnormal_analysis)
# print(abandoned_tasks_3)
abnormal_analysis_statistics = {}  # todo 这里装的是运维次数
for spiderName, abnormal_task in abnormal_analysis.items():
    for task in abnormal_task:
        abnormal_analysis_statistics[task] = abnormal_analysis_statistics.get(task, 0) + 1
# print(abnormal_analysis_statistics)
# print(len(abandoned_tasks_2))

def get_time_format(timestamp):
    time_format_1 = '%d年%d月'
    time_format_2 = '%d年%d月%d日'
    import datetime
    current_time = datetime.datetime.fromtimestamp(timestamp)
    return time_format_1 % (current_time.year, current_time.month), time_format_2 % (current_time.year, current_time.month, current_time.day)
def sorted_tasks(tasks: list, key=lambda task: task['time']) -> list:
    return sorted(tasks, key=key)
# def get_month_statistics(tasks):
#     time_format = '%d年%d月'
#     statistics_tasks_4 = dict()
#     for spiderName, spider_task in tasks.items():
#         if len(spider_task) > 1:
#             _abnormal_analysis = {}
#             for task in spider_task:
#                 if task['rwzt'] in operations_states:
#                     current_time = datetime.fromtimestamp(task['time'])
#                     current_year = current_time.year
#                     current_month = current_time.month
#                     current = time_format % (current_year, current_month)
#                     _abnormal_analysis[current] = _abnormal_analysis
#             statistics_tasks_4.setdefault(spiderName, [time_diff//2592000, sorted(spider_task, key=lambda task: task['time'])[-1]['time']])# z怎么是最后一次的时间
#     plot_line_x_values = []
#     plot_line_y_values = []
#     statistics_tasks_4 = sorted(statistics_tasks_4.values(), key=lambda x: x[1])
#     for spider_task in statistics_tasks_4:
#         plot_line_x_values.append(spider_task[1])
#         plot_line_y_values.append(spider_task[0])
#     time_format = '%d年%d月'
#     statistics = OrderedDict()
#     for index, value in enumerate(plot_line_x_values):
#         current = datetime.fromtimestamp(value)
#         current_year = current.year
#         current_month = current.month
#         current = time_format % (current_year, current_month)
#         statistics[current] = statistics.get(current, 0) + 1
#     return statistics
# print(get_month_statistics(abandoned_tasks_2))
def get_month_statistics(tasks):
    statistics = dict()
    for spiderName, spider_task in tasks.items():
        normal_info = OrderedDict()
        detail_info = OrderedDict()
        start = None
        for task in sorted_tasks(spider_tasks[spiderName]):
            if not start and task['rwzt'] in complete_states:
                start = task['time']
                _time = get_time_format(task['time'])
                normal_info[_time[0]] = 0
                detail_info[_time[1]] = 0
                continue
            if start and task['rwzt'] in operations_states:
                _time = get_time_format(task['time'])
                normal_info[_time[0]] = 1
                detail_info[_time[1]] = 1
        statistics[spiderName] = [normal_info, detail_info]
    return statistics
# print(get_month_statistics(abandoned_tasks_2))

def get_abandoned_spider_statistics(tasks):
    abandoned_tasks = dict()
    for spiderName, spider_task in tasks.items():
        abandoned_tasks.setdefault(spiderName, sorted(spider_task, key=lambda task: task['time'])[-1]['time'])
    abandoned_tasks = sorted(abandoned_tasks.values(), key=lambda x: x)
    statistics = OrderedDict()
    for value in abandoned_tasks:
        current = get_time_format(value)[0]
        statistics[current] = statistics.get(current, 0) + 1
    return statistics
abandoned_tasks_3_month_statistics = get_abandoned_spider_statistics(abandoned_tasks_3)  # 废弃爬虫统计

# storage_tasks
import datetime
def completion_time(operations):
    date_template = OrderedDict()
    start = operations.pop('start')
    last = operations.pop('last')
    time_format_1 = '%d年%d月'
    start = datetime.datetime.fromtimestamp(start)
    last = datetime.datetime.fromtimestamp(last)
    year = start.year
    month = start.month
    now_year = last.year
    now_month = last.month
    while year <= now_year:
        if month < 13:
            date_template[time_format_1 % (year, month)] = 0
            if year == now_year and month == now_month:
                break
            month += 1
        else:
            year += 1
            month = 1
            date_template[time_format_1 % (year, month)] = 0
    return date_template

def get_all_operations_times(tasks):
    all_operations = dict()
    for spiderName, spider_task in tasks.items():  # 遍历每一个已入库的爬虫
        start = None
        operations = dict()
        spider_task = sorted(spider_task, key=lambda task: task['time'])
        for task in spider_task:
            if not start and task['rwzt'] in complete_states:
                start = task['time']
                operations['start'] = task['time']
                continue
            if start:
                if spiderName in abandoned_tasks_3:
                    operations['last'] = spider_task[-1]['time']
                else:
                    operations['last'] = time.time()
                break
        if start and len(operations) == 1:
            operations['last'] = time.time()
        operations = completion_time(operations)
        all_operations[spiderName] = operations
    return all_operations
all_tasks_3_month_statistics = get_all_operations_times(storage_tasks)

def get_abnormal_spider_tasks_statistics(tasks):
    all_abnormal_statistics = dict()
    for spiderName, spider_task in tasks.items():
        start = None
        abnormal_statistics = dict()
        for task in spider_task:
            if not start and task['rwzt'] in complete_states:
                start = True
                continue
            if start and task['rwzt'] in operations_states:
                cur = get_time_format(task['time'])[0]
                abnormal_statistics[cur] = abnormal_statistics.get(cur, 0) + 1
        if abnormal_statistics:
            all_abnormal_statistics[spiderName] = abnormal_statistics
    return all_abnormal_statistics
abnormal_spider_tasks_statistics = get_abnormal_spider_tasks_statistics(abandoned_tasks_2)

def get_date_template(check_start_year, check_start_month):
    date_template = OrderedDict()
    time_format_1 = '%d年%d月'
    now = datetime.datetime.now()
    year, month = now.year, now.month
    while check_start_year <= year:
        if check_start_month < 13:
            date_template[time_format_1 % (check_start_year, check_start_month)] = 0
            if check_start_year == year and check_start_month == month:
                break
            check_start_month += 1
        else:
            check_start_year += 1
            check_start_month = 1
            date_template[time_format_1 % (check_start_year, check_start_month)] = 0
    return date_template
date_template = get_date_template(2018, 1)

from copy import deepcopy
def get_statistics_into_template(date_template, tasks, add=True):
    _date_template = deepcopy(date_template)
    for spiderName, spider_task in tasks.items():
        if isinstance(spider_task, int):
            _date_template[spiderName] = _date_template.get(spiderName, 0) + spider_task
            continue
        for task, value in spider_task.items():
            if task in _date_template:
                if add:
                    _date_template[task] = _date_template.get(task, 0) + value
                else:
                    _date_template[task] = _date_template.get(task, 0) + 1
    return _date_template
print(get_statistics_into_template(date_template, all_tasks_3_month_statistics, add=False))
print(get_statistics_into_template(date_template, abnormal_spider_tasks_statistics))
print(get_statistics_into_template(date_template, abandoned_tasks_3_month_statistics))
