import json
import pandas as pd
from pandas import *

from collections import defaultdict, OrderedDict
from copy import deepcopy
from pylab import *

mpl.rcParams['font.sans-serif'] = ['SimHei']

# 状态管理
demand_states = {'任务已分发', '驳回运维意见', '待处理'}
developer_states = {'初爬通过', '正在开发', '自查完成', '正在下载源码', '正在修改', '代码完成',
                    '解析完成', '请求撤回提交', '开发完成', '源码下载完成', '疑难网站',
                    '提交任务', '初爬完成', '研发修改完成', '驳回测试修改意见', '正在解析'}
cleaning_states = {'文件清洗完成', '正在清洗', '清洗修改完成'}
test_states = {'测试查完成', '测试挂起', '正在测试', '初测通过', '返回清洗修改', '返回修改', '请清洗文件', '请重新下源码', '源码有问题'}
storage_states = {'返回修改', '入库复核通过', '入库失败', '入库完成', '正在入库', '不入库', '数据已转移', '暂不入库',
                  '重跑一遍', '重跑完成', '特殊入库'}
operations_states = {'网站异常', '停止维护', '全网查完成', '无增量挂起', '废弃需求', '运维发现异常', '驳回需求', '返回修改'}
# 特殊状态
abandoned_states = {'停止维护', '废弃需求'}
complete_states = {'入库完成', '特殊入库', '数据已转移', '入库复核通过'}
event_state = ['需求', '开发', '测试', '清洗', '入库', '运维']
multi_table = {"诚信数据": 1, "法律": 2, "新闻": 3, "钢铁": 5, "政府网站": 6, "零碎任务": 7, "航运": 8}


def get_data(name, version=1, flag=False):
    try:
        with open('%s.json' % name, 'r', encoding='utf-8') as json_file:
            return json.loads(json_file.read())[name]
    except FileNotFoundError:
        if flag:
            raise Exception('二次加载数据失败！')
        try:
            from mysql_database import get_version_data
            return get_version_data(name, version, save=False)[name]
            # return get_data(name, version, True)
        except:
            raise Exception('没有对应的JSON文件，也没有加载数据的代码，请联系开发！')


def get_spider_tasks(data_list, dupefilter=()):
    spider_tasks = defaultdict(list)
    for data in data_list:
        if data['spiderName'] in dupefilter:
            continue
        spider_tasks[data['spiderName']].append(data)
    for key, value in spider_tasks.items():
        value.sort(key=lambda x: x['time'])
    return spider_tasks


def get_event_info(tasks):
    event_name_value = dict()
    first_storage_event_name_value = dict()
    operation_tasks = dict()
    abandoned_tasks = dict()
    storage_tasks = dict()
    first_storage_time_range = dict()
    for spiderName, spider_task in tasks.items():
        _event = [0 for _ in range(len(event_state))]
        _event2 = [0 for _ in range(len(event_state))]
        if spider_task[-1]['rwzt'] in abandoned_states:  # 最后一个任务状态处于废弃，则认为是废弃爬虫
            abandoned_tasks.setdefault(spiderName, spider_task)
        first_storage = False
        first_task_time = first_storage_time = None
        for task in spider_task:
            if not first_task_time and task['rwzt'] in developer_states:
                first_task_time = task['time']
            if spiderName not in operation_tasks and task['rwzt'] in operations_states:  # 该爬虫有过运维经历
                operation_tasks.setdefault(spiderName, spider_task)
            if spiderName not in storage_tasks and task['rwzt'] in complete_states:  # 该爬虫有过入库经历
                first_storage = True
                storage_tasks.setdefault(spiderName, spider_task)
                if not first_storage_time:
                    first_storage_time = task['time']
            for index, state in enumerate(
                    [demand_states, developer_states, cleaning_states, test_states, storage_states,
                     operations_states]):  # 统计各个经历的次数
                if not first_storage and task['rwzt'] in state:
                    _event2[index] = _event2[index] + 1
                if task['rwzt'] in state:
                    _event[index] = _event[index] + 1
                    break
        event_name_value.setdefault(spiderName, _event)
        first_storage_event_name_value.setdefault(spiderName, _event2)
        first_storage_time_range.setdefault(spiderName, [first_task_time, first_storage_time])
    return event_name_value, operation_tasks, abandoned_tasks, storage_tasks, first_storage_event_name_value, \
           first_storage_time_range


# 工具类方法
def get_time_format(timestamp):
    time_format_1 = '%d年%d月'
    time_format_2 = '%d年%d月%d日'
    current_time = datetime.datetime.fromtimestamp(timestamp)
    return time_format_1 % (current_time.year, current_time.month), \
           time_format_2 % (current_time.year, current_time.month, current_time.day)


def sorted_tasks(tasks: list, key=lambda task: task['time']) -> list:
    return sorted(tasks, key=key)


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


def get_life_statistics(tasks):
    life_time = OrderedDict()
    for spiderName, spider_task in tasks.items():
        start_time = None
        first = None
        life_time_statistics = OrderedDict()
        for task in spider_task:
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
                life_time_statistics.setdefault('start_time', task['time'])
        if not life_time_statistics.get('first_time'):
            continue
        if spiderName in abandoned_tasks_3:
            life_time_statistics['total_times'] = ((life_time_statistics['last_time'] - life_time_statistics[
                'start_time']) // 2592000) or 1
            life_time_statistics['is_live'] = False
        else:
            life_time_statistics['total_times'] = ((time.time() - life_time_statistics['start_time']) // 2592000) or 1
            life_time_statistics['is_live'] = True
        if life_time_statistics['total_times'] >= life_time_statistics['abnormal_times']:
            life_time.setdefault(spiderName, life_time_statistics)
    return life_time


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


def get_date_template(check_start_year, check_start_month, end_year=None, end_month=None):
    if all((end_year, end_month)):
        year, month = end_year, end_month
    elif not check_end_date_flag:
        now = datetime.datetime.now()
        year, month = now.year, now.month
    else:
        year, month = check_end_year, check_end_month
    date_template = OrderedDict()
    time_format_1 = '%d年%d月'
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


def get_all_operations_times(tasks):
    all_operations = dict()
    new_tasks = {}
    if check_end_date_flag:
        _check_start_timestamp = check_start_timestamp
        _check_end_timestamp = check_end_timestamp
    else:
        _check_start_timestamp = check_start_timestamp
        _check_end_timestamp = time.time()
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
        start = datetime.datetime.fromtimestamp(operations['start'])
        last = datetime.datetime.fromtimestamp(operations['last'])
        if spiderName in spider_life_time:
            start_time = spider_life_time[spiderName]['start_time']
            last_time = spider_life_time[spiderName]['last_time']
            if not last_time < _check_start_timestamp and not start_time > _check_end_timestamp:
                new_tasks[spiderName] = spider_task
        operations = get_date_template(start.year, start.month, last.year, last.month)
        all_operations[spiderName] = operations
    return new_tasks, all_operations


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


def get_statistics_into_template(date_template, tasks, add=True):
    _date_template = deepcopy(date_template)
    for spiderName, spider_task in tasks.items():
        if isinstance(spider_task, int):
            if spiderName in _date_template:
                _date_template[spiderName] = _date_template.get(spiderName, 0) + spider_task
            continue
        for task, value in spider_task.items():
            if task in _date_template:
                if add:
                    _date_template[task] = _date_template.get(task, 0) + value
                else:
                    _date_template[task] = _date_template.get(task, 0) + 1
    return _date_template


def get_statistics_table(tasks):  # 画pandas图
    farmers = ['需求岗', '开发岗', '清洗岗', '测试岗', '入库岗', '运维岗']
    abandoned_spiderName = set(abandoned_tasks_3.keys())
    abandoned_vegetables = []  # 爬虫任务名
    abandoned_harvest = []  # 爬虫的值
    for spiderName, spider_task in tasks.items():
        if spiderName in abandoned_spiderName:
            abandoned_vegetables.append(spiderName)
            abandoned_harvest.append(spider_task)
    abandoned_harvest = np.array(abandoned_harvest)
    df = pd.DataFrame(abandoned_harvest, columns=farmers)
    df2 = df.describe(percentiles=[])
    df2.loc['count'] = df2.loc['count'].apply(lambda x: str(int(x)))
    return df2


def calcul(task1, task2):
    df = pd.DataFrame(task1 / task2)
    return df.fillna(0).values


def init(name, check_start_date, check_end_date=None, version=1):
    """
    初始化全局参数-此函数内定义均为全局参数。
    下面列出了各个数据的意义与数据结构
    有需要可添加新数据

    task_name:  任务名称 - spiderName
    task_data:  该爬虫任务所有的历史记录 - [{'spiderName': xxx, 'time': xxx, }, spiderEvent2, spiderEvent3...]
    spider_tasks:  对所有记录进行分类汇总 - {'spiderName': [spiderEvent1, spiderEvent2]}
    abandoned_tasks_2:  已入库爬虫中，有过运维异常记录的爬虫任务 - {'spiderName': [spiderEvent1, spiderEvent2]}
    abandoned_tasks_3:  已入库爬虫中，处于废弃状态的爬虫任务 - {'spiderName': [spiderEvent1, spiderEvent2]}
    event_name_value:
    operation_tasks:  经历过运维的爬虫任务 - {'spiderName': [spiderEvent1, spiderEvent2]}
    abandoned_tasks:  处于废弃状态的爬虫任务 - {'spiderName': [spiderEvent1, spiderEvent2]}
    storage_tasks:  历史入库完成的爬虫任务 - {'spiderName': [spiderEvent1, spiderEvent2]}
    check_start_year:  开始时间，年 - eg: 2018
    check_start_month:  开发时间，月 - eg: 1
    check_end_year:  结束时间，年 - eg: 2019
    check_end_month:  结束时间，月 - eg: 1
    check_end_date_flag:  用户是否设定结束时间的标识
    check_start_timestamp:  开始时间 - 时间戳
    check_end_timestamp:  结束时间 - 时间戳
    spider_life_time:  爬虫生命周期 {'spiderName': [第一次开发完成时间, 第一次运维异常时间, 最后一次运维异常时间, 运维次数, 是否废弃]...}
    spider_month_statistics:  爬虫每月运维记录统计
    new_event_name_value_by_date:
    abnormal_spider_tasks_statistics:  爬虫运维异常记录统计
    abandoned_tasks_3_month_statistics:  已废弃爬虫历史运维记录统计
    num_length:  数据长度
    abandoned_num_list:  废弃爬虫每月统计
    abnormal_num_list:  运维异常爬虫每月统计
    all_num_list:  每月运维次数总统计
    """
    global \
        task_name, task_data, spider_tasks, abandoned_tasks_2, abandoned_tasks_3, \
        event_name_value, operation_tasks, abandoned_tasks, storage_tasks, \
        check_start_year, check_start_month, check_end_year, check_end_month, check_end_date_flag, \
        check_start_timestamp, check_end_timestamp, \
        spider_life_time, \
        spider_month_statistics, new_event_name_value_by_date, abnormal_spider_tasks_statistics, abandoned_tasks_3_month_statistics, \
        num_length, abandoned_num_list, abnormal_num_list, all_num_list, tasks_tables, tasks_tables_labels, labels, \
        first_storage_event_name_value, first_storage_time_range
    task_name = name
    if '.' in check_start_date and check_start_date.count('.') < 2:
        check_start_year, check_start_month = [int(date) for date in check_start_date.split('.')]
    else:
        check_start_year = int(check_start_date)
        check_start_month = 1
    check_start_timestamp = int(datetime.datetime(check_start_year, check_start_month, 1).timestamp())
    try:
        if check_end_date:
            if '.' in check_end_date and check_end_date.count('.') < 2:
                check_end_year, check_end_month = [int(date) for date in check_end_date.split('.')]
            else:
                check_end_year = int(check_start_date)
                check_end_month = 1
            check_end_timestamp = int(datetime.datetime(check_end_year, check_end_month, 1).timestamp())
            check_end_date_flag = 1
        else:
            check_end_date_flag = 0
    except:
        check_end_date_flag = 0
    task_data = get_data(task_name, version=version)
    spider_tasks = get_spider_tasks(task_data)
    event_name_value, operation_tasks, abandoned_tasks, storage_tasks, first_storage_event_name_value, \
    first_storage_time_range = get_event_info(spider_tasks)
    abandoned_tasks_2 = dict()  # 历史入库完成的爬虫中，经历运维的爬虫任务
    abandoned_tasks_3 = dict()  # 历史入库完成的爬虫中，被废弃的爬虫任务
    for spiderName, spider_task in storage_tasks.items():
        start = None
        for task in spider_task:
            if not start and task['rwzt'] in complete_states:
                start = True
                continue
            if start:
                if spiderName not in abandoned_tasks_2 and task['rwzt'] in operations_states:
                    abandoned_tasks_2.setdefault(spiderName, spider_task)
            if spiderName not in abandoned_tasks_3 and task['rwzt'] in abandoned_states:
                abandoned_tasks_3.setdefault(spiderName, spider_task)

    spider_life_time = get_life_statistics(abandoned_tasks_2)  # 运维爬虫中的 各项指标统计
    spider_month_statistics = get_month_statistics(abandoned_tasks_2)  # 开始时间与运维异常时间
    new_task_by_date, all_tasks_3_month_statistics = get_all_operations_times(storage_tasks)  # 运维总次数
    new_event_name_value_by_date = get_event_info(new_task_by_date)[0]
    abnormal_spider_tasks_statistics = get_abnormal_spider_tasks_statistics(abandoned_tasks_2)  # 运维异常统计
    abandoned_tasks_3_month_statistics = get_abandoned_spider_statistics(abandoned_tasks_3)  # 废弃爬虫统计
    date_template = get_date_template(check_start_year, check_start_month)
    all_into_template = get_statistics_into_template(date_template, all_tasks_3_month_statistics, add=False)
    abnormal_into_template = get_statistics_into_template(date_template, abnormal_spider_tasks_statistics)
    abandoned_into_template = get_statistics_into_template(date_template, abandoned_tasks_3_month_statistics)
    labels = all_into_template.keys()
    all_num_list = all_into_template.values()
    abnormal_num_list = abnormal_into_template.values()
    abandoned_num_list = abandoned_into_template.values()
    num_length = len(all_num_list)
    tasks_tables = [
        ['%s总记录' % task_name, len(task_data)],
        ['%s总任务' % task_name, len(spider_tasks)],
        ['有过运维记录的任务', len(operation_tasks)],
        ['处于废弃状态的任务', len(abandoned_tasks)],
        ['历史入库完成任务', len(storage_tasks)],
        ['运维(历史入库完成)', str(len(abandoned_tasks_2)) + '({}%)'.format(
            int(len(abandoned_tasks_2) / len(storage_tasks) * 100))],
        ['废弃(历史入库完成)', str(len(abandoned_tasks_3)) + '({}%)'.format(
            int(len(abandoned_tasks_3) / len(storage_tasks) * 100))],
    ]
    tasks_tables_labels = ['', 'count']


def get_data_first():
    return [
        ['{}总记录'.format(task_name), len(task_data)],
        ['{}总任务'.format(task_name), len(spider_tasks)],
        ['{}有过运维记录的任务'.format(task_name), len(operation_tasks)],
        ['{}处于废弃状态的任务'.format(task_name), len(abandoned_tasks)],
        ['{}历史入库完成任务'.format(task_name), len(storage_tasks)],
        ['入库任务中运维发现异常的任务', len(abandoned_tasks_2),
         '{}%'.format(int(len(abandoned_tasks_2) / len(storage_tasks) * 100))],
        ['入库任务中运维废弃的任务'.format(task_name), len(abandoned_tasks_3),
         '{}%'.format(int(len(abandoned_tasks_3) / len(storage_tasks) * 100))],
    ]


def get_data_second():
    global df_spider
    spider_operations_time_keys = spider_life_time.keys()
    spider_operations_time_value = []
    columns = []
    for spiderName, tasks in spider_life_time.items():
        if not columns:
            columns = tasks.keys()
        spider_operations_time_value.append(list(tasks.values()))
    spider_operations_time = np.array(spider_operations_time_value)
    df_spider = pd.DataFrame(spider_operations_time, index=spider_operations_time_keys, columns=columns)
    df_spider['start_time'] = df_spider['start_time'].apply(lambda x: get_time_format(x)[0])
    df_spider['first_time'] = df_spider['first_time'].apply(lambda x: get_time_format(x)[0])
    df_spider['last_time'] = df_spider['last_time'].apply(lambda x: get_time_format(x)[0])
    df_spider['is_live'] = df_spider['is_live'].apply(lambda x: True if x else False)
    df3 = df_spider.describe(percentiles=[])
    df3['pre'] = '-'
    df3.loc['mean', 'pre'] = str(int((df3.loc['mean', 'abnormal_times'] / df3.loc['mean', 'total_times']) * 100)) + '%'
    _label = list(df3.index[1:])
    # return [list(li) for li in df3.values[1:]]
    return [[_label[index]] + list(li) for index, li in enumerate(df3.values[1:])]


def get_data_third():
    return [list(labels), list(abandoned_num_list), list(abnormal_num_list), list(all_num_list)]


def get_data_fourth():
    all_range_day = 0
    all_people = 0
    count = 0
    for key, value in first_storage_event_name_value.items():
        start, end = first_storage_time_range[key]
        a, b, c, d, e, f = value
        people = sum([max(b / 2, 1), c, max(d / 2, 1), e, f])  # 开发和测试次数，除以2
        try:
            range_day = int((end - start) / 86400)
            all_range_day += range_day
            all_people += people
            count += 1
        except:
            pass
    return [task_name, count, int(all_range_day / count), int(all_people / count)]


if __name__ == '__main__':
    import json

    init('诚信数据', '2019.01', version=1)
    # print(json.dumps(get_data_first()))
    # print(get_data_second())
    # json.dumps(get_data_second())
    # print(get_data_third())
    # print(get_data_fourth())
    # pprint(event_name_value)  # 任务 + 各阶段统计次数
    # pprint(storage_tasks)  # 任务名字 + 该任务的所有记录
    # pprint(first_storage_event_name_value)
