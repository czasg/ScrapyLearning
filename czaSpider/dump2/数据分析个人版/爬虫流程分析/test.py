import json
from collections import defaultdict
dupefilter = ['疑难网站', '网站异常', '驳回需求', '运维发现异常', '废弃需求', '停止维护', '网站异常']
basic_state = ['正在开发', '开发完成', '清洗修改完成', '正在测试', '测试查完成', '正在入库', '入库完成', '研发修改完成', '返回修改']

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
        self.data = data
        self.developer_time = 0
        self.developer_times = 0
        self.tester_time = 0
        self.tester_times = 0
        self.storager_time = 0
        self.storager_times = 0
    def _get_state_time(self, state):
        state = state if isinstance(state, list) else [state]
        flag = use = 0
        for i, j in enumerate(self.data):
            if j[self.state] == state:
                flag = i + 1
                use = j[self.time]
                try:
                    if self.data[flag][self.state] in state:
                        continue
                except:
                    break
                self.data = self.data[flag:]
                break
        if not flag:
            raise Exception()
        return use

    def get_developer(self):
        time1 = self._get_state_time('正在开发')
        time2 = self._get_state_time('开发完成')
        self.developer_time += (time2 - time1)

    def get_tester(self):
        time1 = self._get_state_time('清洗修改完成')
        time2 = self._get_state_time(['返回修改', '测试查完成'])
    def get_storager(self):
        pass
    def process(self):
        pass
if __name__ == '__main__':
    aim = "人事变动"
    data = get_data(aim)
    # print(data)
    hard_spider_name = get_hard_spider_name(data[aim])
    # print(get_task_state(data[aim]))
    # print(get_spider_tasks(data[aim]))

    all_spider_tasks = get_spider_tasks(data[aim], hard_spider_name)
    for spider_name, spider_tasks in all_spider_tasks.items():
        tasks = sorted(spider_tasks, key=lambda data: data['time'])  # 按时间进行排序
        # print(tasks)
        # development = 0
        # development_success = 0
        basic = []
        for index, task in enumerate(tasks):
            # if not development and task['rwzt'] == '正在开发':
            #     development = index
            if task['rwzt'] in basic_state:
                basic.append(task)
        print(basic)

        flag = 0
        use = 0
        for i,j in enumerate(basic):
            if j['rwzt'] == '正在开发':
                flag = i+1
                use = j['time']
                basic = basic[flag:]
        if not flag:
            break

        for t in basic:
            pass


        break


