import json
import numpy as np
from collections import defaultdict, deque
from copy import deepcopy
from importlib import import_module
trees=import_module('tree')
dupefilter = ['疑难网站', '网站异常', '驳回需求', '运维发现异常', '废弃需求', '停止维护', '网站异常']
basic_state = ['正在开发', '开发完成', '清洗修改完成', '正在测试', '测试查完成', '正在入库', '入库完成', '研发修改完成', '返回修改']
minute=60
hour=minute*60
day=hour*24
two_day=day*2
five_day=day*5
# print(day, two_day, five_day)
good=1
normal=2
whats=3
class AbnormalTask(Exception): ...
def get_data(name):
    with open('%s.json' % name, 'r', encoding='utf-8') as json_file:
        return json.loads(json_file.read())
def get_hard_spider_name(data_list):
    hard_spider = set()
    for data in data_list:
        if data['rwzt'] in dupefilter or data['spiderName'].count('-') != 2:
            hard_spider.add(data['spiderName'])
    return hard_spider

def get_task_state(data_list, dupefilter=()):
    task_state = defaultdict(list)
    for data in data_list:
        if data['spiderName'] in dupefilter:
            continue
        if data['rwzt'] in basic_state:
            task_state[data['rwzt']].append(data)
    return task_state

def get_spider_tasks(data_list, dupefilter=()):
    spider_tasks = defaultdict(list)
    for data in data_list:
        if data['spiderName'] in dupefilter:
            continue
        spider_tasks[data['spiderName']].append(data)
    return spider_tasks

class Test:
    state = 'rwzt'
    time = 'time'
    def __init__(self, data):
        self.source = deepcopy(data)
        self.data = data
        self.developer_time = 0
        self.developer_times = 0
        self.tester_time = 0
        self.tester_times = 0
        self.storager_time = 0
        self.storager_times = 0
    def process_dict(self):
        developer_time = self.developer_time//self.developer_times
        tester_time = self.tester_time//self.tester_times
        storager_time = self.storager_time//self.storager_times
        return dict(developer_time=developer_time,
                    developer_times=self.developer_times,
                    tester_time=tester_time,
                    tester_times=self.tester_times,
                    storager_time=storager_time,
                    storager_times=self.storager_times,
                    total_time=developer_time+tester_time+storager_time)
    def _get_state_time(self, state):
        if not isinstance(state, tuple) and not isinstance(state, list):
            state = [state]
        flag = time_use = label = None
        for index, data in enumerate(self.data):
            if data[self.state] in state:
                flag = index + 1
                time_use = data[self.time]
                try:
                    label = data[self.state]
                    if self.data[flag][self.state] in state:
                        continue
                except:
                    break
                self.data = self.data[index:]
                break
        if not flag:
            raise AbnormalTask
        return time_use, label
    def _process_task(self, start, end):
        time1, label1 = self._get_state_time(start)
        time2, label2 = self._get_state_time(end)
        return time2-time1, label2
    def check_tester_wrong(self, state1=('驳回测试修改意见', '清洗修改完成'), state2=('驳回测试修改意见')):
        try:
            return self.data[1][self.state] in state1 or \
                   self.data[2][self.state] in state2
        except:
            raise AbnormalTask
    def check_storager_wrong(self, state1=('正在入库')):
        try:
            return self.data[1][self.state] in state1
        except:
            raise AbnormalTask
    def get_developer(self, start=('开发完成','返回修改'), end=('开发完成','研发修改完成')):
        if self.check_tester_wrong():
            return self.get_tester()
        elif self.check_tester_wrong(('正在测试')):
            return self.get_tester(('正在测试'))
        elif self.check_storager_wrong():
            return self.get_storager(('返回修改'), ('入库完成'))
        else:
            time_diff, label = self._process_task(start, end)
        self.developer_time += time_diff
        self.developer_times += 1
        return label
    def get_tester(self, start=('清洗修改完成', '驳回测试修改意见'), end=('返回修改', '测试查完成')):
        time_diff, label = self._process_task(start, end)
        self.tester_time += time_diff
        self.tester_times += 1
        return label
    def get_storager(self, start=('测试查完成'), end=('返回修改', '入库完成')):
        time_diff, label = self._process_task(start, end)
        self.storager_time += time_diff
        self.storager_times += 1
        return label
    def process_label(self, label):
        if label in ['返回修改']:
            label = self.get_developer()
        elif label in ['开发完成', '研发修改完成']:
            label = self.get_tester()
        elif label in ['测试查完成']:
            label = self.get_storager()
        elif label in ['入库完成']:
            return
        self.process_label(label)
    def process(self):
        time_diff, label = self._process_task(['待处理','正在开发'], ['开发完成'])
        self.developer_time += time_diff
        self.developer_times += 1
        self.process_label(label)
        return self
if __name__ == '__main__':
    # aim = "人事变动"
    aim = "领导之窗"
    data = get_data(aim)
    # print(data)
    hard_spider_name = get_hard_spider_name(data[aim])
    # print(get_task_state(data[aim]))
    # print(get_spider_tasks(data[aim]))

    labels=deque()
    dataSets=[]
    all_spider_tasks = get_spider_tasks(data[aim], hard_spider_name)
    for spider_name, spider_tasks in all_spider_tasks.items():
        tasks = sorted(spider_tasks, key=lambda data: data['time'])  # 按时间进行排序
        # print(tasks)
        try:
            a = Test(tasks).process()
        except AbnormalTask:
            # print(tasks)
            continue
        # print(a.developer_time)
        # print(a.developer_times)
        # print(a.tester_time)
        # print(a.tester_times)
        # print(a.storager_time)
        # print(a.storager_times)
        # print(a.process_dict())

        b = a.process_dict()
        for key in ['developer_time','tester_time','storager_time','total_time']:
            if key == 'total_time':
                if b[key] < two_day:
                    b[key] = 'good'
                elif b[key] < five_day:
                    b[key] = 'normal'
                else:
                    b[key] = 'whats'
                continue
            if b[key] < two_day:
                b[key] = 1
            elif b[key] < five_day:
                b[key] = 2
            else:
                b[key] = 3
        # print(b)
        for key in ['developer_times','tester_times','storager_times']:
        #     b.pop(key)
            if b[key] < 2:
                b[key] = 1
            elif b[key] < 4:
                b[key] = 2
            else:
                b[key] = 3
        # for key in ['developer_time','tester_time','storager_time']:
        #     b.pop(key)


        keys = b.keys()
        if not labels:
            for key in keys:
                if key == 'total_time':
                    labels.append(key)
                else:
                    labels.appendleft(key)
                # labels.append(key)  # todo, 我不能保存最后一个就是我需要的total_time，这个需要管控下



        dataSet=[]
        for label in labels:
            dataSet.append(b.pop(label))
        dataSets.append(dataSet)
        # print(dataSet)

        # development = 0
        # development_success = 0
        # basic = []
        # for index, task in enumerate(tasks):
        #     # if not development and task['rwzt'] == '正在开发':
        #     #     development = index
        #     if task['rwzt'] in basic_state:
        #         basic.append(task)
        # print(basic)

        # flag = 0
        # use = 0
        # for i,j in enumerate(basic):
        #     if j['rwzt'] == '正在开发':
        #         flag = i+1
        #         use = j['time']
        #         basic = basic[flag:]
        # if not flag:
        #     break
        #
        # for t in basic:
        #     pass

        # for key in ['developer_time','tester_time','storager_time']:
        #     b.pop(key)


        # break

    # dataSets = np.array(dataSets)
    # print(dataSets)
    # print(np.array(dataSets).shape)
    labels.pop()
    # print(labels)
    # trees.test()
    import pprint
    # print(dataSets)
    # print('----'*50)
    pprint.pprint(trees.createTree(dataSets, list(labels)))
    # print(trees.createTree(dataSets, list(labels)))  # todo, 可视化一下，这个太难看了把