import threading
from collections import Counter
from django.shortcuts import render
from django.http import JsonResponse, Http404

from mini import miniCache

try:
    from database import *
    from base_tools import init, multi_table, get_data_first, get_data_second, get_data_third, get_data_fourth
except:
    raise Exception('没有数据库配置文件，无法运行哦')


def index(request):
    return render(request, 'index.html')


def _get_split_bar(max_value):
    value = (max_value // 10 + 1) * 10
    four = int(value // 4)
    return [
        {'start': four * 3, 'end': value},
        {'start': four * 2, 'end': four * 3},
        {'start': four, 'end': four * 2},
        {'start': 0, 'end': four}
    ]


def _merge_list(*args):
    res = []
    for li in args:
        res.extend(li)
    return res


def _counter_filter(value, finish=5):
    res = []
    count = 0
    for k, v in Counter(value).most_common(len(value)):
        if len(k) > 1:
            if count == finish:
                break
            count += 1
            res.append(k)
    return res


def _query_new_data(query_day, coll='map_data', filter_province=''):
    province = {}
    normal_spider_list = []
    abnormal_spider_list = []
    result, all_jieba_dict = \
        get_collection_statistical('新闻(新闻)', '人民政府', ['标题'], query_day, False, False, filter_province)
    for collection, doc in result.items():
        province[doc['province']] = province.get(doc['province'], 0) + doc['count']
        if doc['count']:
            normal_spider_list.append((collection, doc['count']))
        else:
            abnormal_spider_list.append((collection, doc['count']))
    json_data = json.dumps({
        'map_data': [dict(name=name, value=value) for name, value in province.items()],
        'bar': _get_split_bar(max(province.values())),
        'cloud_data': [dict(name=name, value=value)
                       for name, value in Counter(_merge_list(*all_jieba_dict.values())).items()
                       if len(name.strip()) > 1],
        'normal_spider_list': sorted(normal_spider_list, key=lambda x: x[1], reverse=True),
        'abnormal_spider_list': sorted(abnormal_spider_list, key=lambda x: x[1], reverse=True),
        'current_day': RE_SEARCH_DAY(str(query_day)).group(1),
        'province_cloud_data': {key: _counter_filter(value) for key, value in all_jieba_dict.items()}
    }, ensure_ascii=False)
    mongodb_offline.client['新闻存储-offline'][coll].update_one({'timestamp': int(query_day.timestamp())}, {'$set': {
        'timestamp': int(query_day.timestamp()),
        'json_data': json_data,
    }}, upsert=True)
    return json_data


@miniCache(60 * 5)
def api_get_map_data_v1(request):
    filter_province = '0000' if request.GET.get('just_choose_province', None) == 'true' else ''
    get_day = int(request.GET.get('day', 0))
    if not get_day:
        return Http404()
    query_day = datetime.fromtimestamp(get_day)
    if filter_province:
        coll = 'map_data_province'
    else:
        coll = 'map_data'
    if mongodb_offline.client['新闻存储-offline'][coll].count({'timestamp': int(query_day.timestamp())}):
        threading.Thread(target=_query_new_data, args=(query_day, coll, filter_province)).start()
        json_data = \
            mongodb_offline.client['新闻存储-offline'][coll].find_one({'timestamp': int(query_day.timestamp())},
                                                                  {'json_data': 1, '_id': 0})['json_data']
        return JsonResponse(json.loads(json_data))
    else:
        return JsonResponse(json.loads(_query_new_data(query_day, coll, filter_province)))  # todo BUG，无法保证是最新的数据


@miniCache(60 * 60 * 3)
def api_get_operation_data(request):
    task_name = request.GET.get('task_name', None)
    if not task_name or task_name not in multi_table: return Http404()
    now = get_now_datetime()
    coll = 'operation_data'

    def _query_operation_data(task_name):
        init(task_name, '{}.01'.format(now.year), version=multi_table[task_name])
        json_data = json.dumps({
            'data_summary': get_data_first(),
            'data_statistical': get_data_second(),
            'data_bar': get_data_third(),
            'data_spider_task_statistical': get_data_fourth(),
        }, ensure_ascii=False)
        mongodb_offline.client['新闻存储-offline'][coll].update_one({'task_name': task_name}, {'$set': {
            'task_name': task_name,
            'json_data': json_data,
        }}, upsert=True)
        return json_data

    if mongodb_offline.client['新闻存储-offline'][coll].count({'task_name': task_name}):
        threading.Thread(target=_query_operation_data, args=(task_name,)).start()
        json_data = \
            mongodb_offline.client['新闻存储-offline'][coll].find_one(
                {'task_name': task_name}, {'json_data': 1, '_id': 0})['json_data']
        return JsonResponse(json.loads(json_data))
    else:
        return JsonResponse(json.loads(_query_operation_data(task_name)))
